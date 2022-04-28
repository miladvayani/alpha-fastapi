import phonenumbers
from ..i18n import _
from ..mongo import Mongo
from fastapi import HTTPException
from bson import ObjectId


def validate_mobile_number(mobile):
    try:
        z = phonenumbers.parse(mobile, "IR")
        if mobile[0] != "9":
            raise ValueError(_("Mobile Number is Invalid"))
        if not phonenumbers.is_valid_number(z):
            raise ValueError(_("Mobile Number is Invalid"))
    except phonenumbers.NumberParseException:
        raise ValueError(_("Mobile Number is Invalid"))
    except:
        raise ValueError(_("Mobile Number is Invalid"))
    return mobile


def validate_phone_number(mobile):
    try:
        z = phonenumbers.parse(mobile, "IR")
        if mobile[0] == "9":
            raise ValueError(_("Phone Number is Invalid"))
        if not phonenumbers.is_valid_number(z):
            raise ValueError(_("Phone Number is Invalid"))
    except phonenumbers.NumberParseException:
        raise ValueError(_("Phone Number is Invalid"))
    except:
        raise ValueError(_("Phone Number is Invalid"))
    return mobile


def validate_national_code(nc):
    """
    algorithm for check that national number is right
    """
    if len(nc) != 10:
        raise ValueError(_("Invalid Buyer id"))
    try:
        int(nc)
    except (TypeError, ValueError):
        raise ValueError(_("Invalid Buyer id"))
    not_national = list()
    for i in range(0, 10):
        not_national.append(str(i) * 10)
    if nc in not_national:
        raise ValueError(_("Invalid Buyer id"))
    total = 0
    nc_p = nc[:9]
    i = 0
    for c in nc_p:
        total = total + int(c) * (10 - i)
        i = i + 1
    rem = total % 11
    if rem < 2:
        if int(nc[9]) != rem:
            raise ValueError(_("Invalid Buyer id"))
    else:
        if int(nc[9]) != 11 - rem:
            raise ValueError(_("Invalid Buyer id"))
    return nc


def validate_national_id(ni):
    if len(ni) != 11:
        raise ValueError(_("National ID is Invalid"))
    try:
        int(ni)
    except (TypeError, ValueError):
        raise ValueError(_("National ID is Invalid"))
    ni_p = ni[:10]
    control_digit = int(ni[-1])
    decimal = int(ni[-2]) + 2
    total = 0
    i = 0
    multiplier = [29, 27, 23, 19, 17, 29, 27, 23, 19, 17]
    for c in ni_p:
        total += (int(c) + decimal) * multiplier[i]
        i += 1
    result = total % 11
    if result == 10:
        result = 0
    if result != control_digit:
        raise ValueError(_("National ID is Invalid"))
    return ni


def validate_economical_code(ec):
    if not len(ec) == 14:
        raise ValueError(_("Economical Code is Invalid"))
    try:
        int(ec)
    except (TypeError, ValueError):
        raise ValueError(_("Economical Code is Invalid"))
    if not str(ec).startswith("411"):
        raise ValueError(_("Economical Code is Invalid"))
    return ec


async def validate_province_city(dbname: str, province_name: str, city_name: str):
    result = list()
    pipeline = [
        {"$match": {"name": province_name}},
        {
            "$lookup": {
                "from": "city",
                "localField": "code",
                "foreignField": "province_code",
                "as": "city",
            }
        },
        {"$match": {"city": {"$elemMatch": {"name": city_name}}}},
    ]
    documents = Mongo.client[dbname]["province"].aggregate(pipeline)
    async for doc in documents:
        result.append(doc)
    if not result:
        raise HTTPException(
            status_code=400,
            detail={
                "city_name": _("Invalid city"),
                "province_name": _("Invalid province"),
            },
        )


async def validate_group(dbname: str, group_id):
    pipeline = [
        {"$match": {"_id": ObjectId(group_id)}},
        {
            "$lookup": {
                "from": "group",
                "localField": "parent_id",
                "foreignField": "_id",
                "as": "parent",
            }
        },
        {
            "$project": {
                "_id": 0,
                "sub_group_name": "name",
                "group_name": {"$first": "$parent.name"},
            }
        },
    ]
    documents = Mongo.client[dbname]["group"].aggregate(pipeline)
    async for doc in documents:
        return doc


async def validate_job(dbname: str, job_name):
    result = list()
    pipeline = [{"$match": {"name": job_name}}]
    documents = Mongo.client[dbname]["job"].aggregate(pipeline)
    async for doc in documents:
        result.append(doc)
    if not result:
        raise HTTPException(400, detail=_("Selected Job Not Found"))


async def validate_bank(dbname: str, bank_name):
    result = list()
    pipeline = [{"$match": {"name": bank_name}}]
    documents = Mongo.client[dbname]["bank"].aggregate(pipeline)
    async for doc in documents:
        result.append(doc)
    if result:
        result = {"name": result[0].get("name"), "code": result[0].get("code")}
    return result


async def validate_main_unit(dbname: str, unit_name):
    result = list()
    pipeline = [{"$match": {"name": unit_name}}]
    documents = Mongo.client[dbname]["mainUnit"].aggregate(pipeline)
    async for doc in documents:
        result.append(doc)
    if result:
        result = {"name": result[0].get("name"), "code": result[0].get("code")}
    return result


async def validate_imt_detail_commodity(dbname: str, imt_id):
    result = list()
    pipeline = [{"$match": {"_id": ObjectId(imt_id)}}]
    documents = Mongo.client[dbname]["imtCommodityDetail"].aggregate(pipeline)
    async for doc in documents:
        result.append(doc)
    if result:
        result = {
            "name": result[0].get("name"),
            "code": result[0].get("code"),
            "unit_code": result[0].get("unit_code"),
            "unit_name": result[0].get("unit_name"),
        }
    return result


async def validate_imt_detail_service(dbname: str, imt_id):
    result = list()
    pipeline = [{"$match": {"_id": ObjectId(imt_id)}}]
    documents = Mongo.client[dbname]["imtServiceDetail"].aggregate(pipeline)
    async for doc in documents:
        result.append(doc)
    if result:
        result = {"name": result[0].get("persian_name"), "code": result[0].get("code")}
    return result


async def get_guild_info(dbname: str, guild_id):
    guild_id = ObjectId(guild_id)
    doc = await Mongo.client[dbname]["guild"].find_one({"_id": guild_id})
    doc["_id"] = str(doc["_id"])
    return doc


async def get_group_by_parent_id(dbname: str, parent_id):
    result = list()
    pipeline = [
        {"$match": {"parent_id": ObjectId(parent_id)}},
        {"$project": {"_id": 0}},
    ]
    documents = Mongo.client[dbname]["group"].aggregate(pipeline)
    async for doc in documents:
        result.append(doc)
    return result


async def get_country_by_name(dbname: str, name: str):
    document = await Mongo.client[dbname]["group"].find_one({"name": name})
    if document:
        document["_id"] = str(document["_id"])
    return document
