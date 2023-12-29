from typing import Any, Dict, List, Optional, Union, Tuple
from pydantic import BaseModel
from datetime import datetime
import logging
from bson import ObjectId
import bson


class Filter(BaseModel):
    where: Optional[Dict[str, Any]] = {}
    skip: Optional[int] = 0
    limit: Optional[int] = 20
    fields: Optional[Union[List[str], Dict[str, int]]]
    include: Optional[List[Any]]
    sort: Optional[List[Tuple[str, int]]] = []


class BaseRepository:
    @staticmethod
    def preprocess_filter(filter: Filter):
        def convert_str_to_datetime(mydict):
            for key, value in mydict.items():
                if isinstance(value, str):
                    if (
                        len(value) >= 24
                        and value[4] == "-"
                        and value[7] == "-"
                        and value[10] == "T"
                        and value[13] == ":"
                        and value[16] == ":"
                        and value[19] == "."
                    ):
                        try:
                            mydict[key] = datetime.strptime(
                                value, "%Y-%m-%dT%H:%M:%S.%f"
                            )
                        except:
                            pass
                    elif isinstance(value, dict):
                        convert_str_to_datetime(value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                convert_str_to_datetime(item)
                    return mydict

        def convert_str_to_objectid(mydict):
            for key, value in mydict.items():
                if key[-3] in ["Ids", "_id"] or key[-2:] in ["Id", "id"]:
                    try:
                        if isinstance(value, str):
                            mydict[key] = ObjectId(value)
                        elif isinstance(value, list):
                            mydict[key] = [ObjectId(item) for item in value]
                        elif isinstance(value, dict):
                            operator = list(value.keys())[0]
                            if operator in ["$in", "$nin"]:
                                mydict[key] = {
                                    operator: [
                                        ObjectId(item) for item in value[operator]
                                    ]
                                }
                            elif operator in ["$eq", "$ne"]:
                                mydict[key] = {operator: ObjectId(value[operator])}
                    except:
                        logging.error(
                            f"failed to convert filter valu to objectid key: {key}, value: {value}, data: {mydict}"
                        )

                if isinstance(value, dict):
                    convert_str_to_objectid(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            convert_str_to_objectid(item)
            return mydict

        def convert_id_name(mydict):
            if mydict is None:
                return mydict

            items = list(mydict.items())
            for key, value in items:
                if key == "id":
                    mydict["_id"] = value
                    del mydict["id"]
                if isinstance(value, dict):
                    convert_id_name(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            convert_id_name(item)
            return mydict

        def convert_include_to_lookup(mylist):
            if mylist is None:
                return None

            mylookups = []
            for i, item in enumerate(mylist):
                if isinstance(item, dict):
                    # if item is already a lookup or unwind, just append it.
                    if "$lookup" in item or "$unwind" in item:
                        mylookups.append(item)
                        continue

                    # if item is a dict with localField, collection, foreignField, as_value, projectFields, convert it to lookup.
                    local_field = item["localField"]
                    collection_name = ""
                    if "collection" in item:
                        collection_name = item["collection"]
                    else:
                        if local_field[-2:] == "Id":
                            collection_name = local_field[0].upper() + local_field[1:-2]
                        elif local_field[-3:] == "Ids":
                            collection_name = local_field[0].upper() + local_field[1:-3]
                        else:
                            continue
                    foreign_field = "_id"
                    as_value = ""
                    if "as_value" in item:
                        as_value = item["as_value"]
                    else:
                        if local_field[-2:] == "Id":
                            as_value = local_field[:-2]
                        elif local_field[-3:] == "Ids":
                            as_value = local_field[:-3] + "s"
                        else:
                            continue

                    lookup_config = {
                        "from": collection_name,
                        "localField": local_field,
                        "foreignField": foreign_field,
                        "as": as_value,
                    }

                    if "projectFields" in item:
                        project_fields = item["projectFields"]  # ["name", "id"]
                        if "id" in project_fields:
                            project_fields.remove("id")
                            project_fields.append("_id")
                        project_fields = {field: 1 for field in project_fields}
                        lookup_config["pipeline"] = [{"$project": project_fields}]

                    mylookups.append({"$lookup": lookup_config})

                    if local_field[-2:] == "Id":
                        mylookups.append(
                            {
                                "$unwind": {
                                    "path": f"${as_value}",
                                    "preserveNullAndEmptyArrays": True,
                                }
                            }
                        )

                elif isinstance(item, str):
                    if item[-2:] == "Id":
                        collection_name = item[0].upper() + item[1:-2]
                        local_field = item
                        foreign_field = "_id"
                        as_value = item[:-2]

                        mylookups.append(
                            {
                                "$lookup": {
                                    "from": collection_name,
                                    "localField": local_field,
                                    "foreignField": foreign_field,
                                    "as": as_value,
                                }
                            }
                        )
                        mylookups.append(
                            {
                                "$unwind": {
                                    "path": f"${as_value}",
                                    "preserveNullAndEmptyArrays": True,
                                }
                            }
                        )

                    elif item[-3:] == "Ids":
                        collection_name = item[0].upper() + item[1:-3]
                        local_field = item
                        foreign_field = "_id"
                        as_value = item[:-3] + "s"

                        mylookups.append(
                            {
                                "$lookup": {
                                    "from": collection_name,
                                    "localField": local_field,
                                    "foreignField": foreign_field,
                                    "as": as_value,
                                }
                            }
                        )

                    else:
                        # The convention is to use Id or Ids at the end of the field name, so if it is not Id or Ids, it is not included.
                        pass

            return mylookups

        def convert_sort_to_dict(sortdata):
            result = {}
            if sortdata is None:
                return None
            if isinstance(sortdata, list):
                # [["text", 1]]
                for item in sortdata:
                    result[item[0]] = item[1]
            if isinstance(sortdata, dict):
                result = sortdata
            return result

        # ----------------------------------------------

        if not filter:
            filter = Filter()

        if isinstance(filter, dict):
            filter = Filter(**filter)

        # ----------------------------------------------

        filter.fields = convert_id_name(filter.fields)

        if isinstance(filter.fields, list):
            filter.fields = {field: 1 for field in filter.fields}

        # ----------------------------------------------

        filter.where = convert_str_to_objectid(filter.where)
        filter.where = convert_id_name(filter.where)
        filter.where = convert_str_to_datetime(filter.where)

        # ----------------------------------------------

        filter.include = convert_include_to_lookup(filter.include)

        # ----------------------------------------------

        filter.sort = convert_sort_to_dict(filter.sort)

        # ----------------------------------------------

        return filter

    @staticmethod
    def execute_find_filter(collection, filter: Filter):
        filter = BaseRepository.preprocess_filter(filter)
        count_filter = {}
        aggregate_pipeline = []
        if filter.where:
            aggregate_pipeline.append({"$match": filter.where})
            count_filter["where"] = filter.where
        if filter.fields:
            aggregate_pipeline.append({"$project": filter.fields})
        if filter.sort:
            aggregate_pipeline.append({"$sort": filter.sort})
        if filter.skip:
            aggregate_pipeline.append({"$skip": filter.skip})
        if filter.limit:
            aggregate_pipeline.append({"$limit": filter.limit})
        if filter.include:
            lookup_pipelines = filter.include
            aggregate_pipeline += lookup_pipelines
        users = collection.aggregate(aggregate_pipeline)
        user_count = collection.count_documents(count_filter)
        newData = []
        for data in users:
            for key, obje in data.items():
                if isinstance(obje, bson.ObjectId):
                    data[key] = str(obje)
                try:
                    for item, obj in obje.items():
                        if isinstance(obj, bson.ObjectId):
                            data[key][item] = str(obj)
                except Exception as e:
                    pass
            newData.append(data)
        return {"data": newData, "count": user_count}

    @staticmethod
    def execute_create_data(collection, data):
        insert_response = collection.insert_one(data)
        inserted_id = ObjectId(insert_response.inserted_id)
        data["_id"] = inserted_id
        for key, obje in data.items():
            if isinstance(obje, bson.ObjectId):
                data[key] = str(obje)
        return data

    @staticmethod
    def execute_update_data(collection, id, data):
        update_body = BaseRepository.preprocess_to_updatebody(data)
        newData = collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {**update_body}},
        )
        return True

    @staticmethod
    def execute_delete_data(collection, id):
        delete_data = collection.delete_one({"_id": ObjectId(id)})
        return True

    @staticmethod
    def execute_count_filter(collection, filter: Filter):
        filter = BaseRepository.preprocess_filter(filter)
        user_count = collection.count_documents(filter.where)
        return user_count

    @staticmethod
    def execute_find_by_id_filter(collection, _id, filter):
        filter = BaseRepository.preprocess_filter(filter)

        if filter.fields:
            user = collection.find_one({"_id": ObjectId(_id)}, filter.fields)
        else:
            user = collection.find_one({"_id": ObjectId(_id)})
        for key, obje in user.items():
            if isinstance(obje, bson.ObjectId):
                user[key] = str(obje)
        return user

    @staticmethod
    def preprocess_to_updatebody(target_item):
        if not isinstance(target_item, dict):
            target_item = target_item.dict()
        update_body = {}
        for key, value in target_item.items():
            if value is not None:
                update_body[key] = value
        if "createdAt" in update_body:
            del update_body["createdAt"]
        return update_body
