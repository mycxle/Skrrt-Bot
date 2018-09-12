import secrets
import pyrebase
import helpers


class Security:
    def __init__(self, db):
        self.db = db
        self.root = "security"
        self.settings = {
            "autofilter_trigger": helpers.db_get(db, self.root+"/autofilter_trigger"),
            "is_locked_channels": helpers.db_get(db, self.root+"/is_locked_channels"),
            "is_locked_server": helpers.db_get(db, self.root+"/is_locked_server"),
            "newaccounts_age": helpers.db_get(db, self.root+"/newaccounts_age"),
            "whitelist": helpers.db_get(db, self.root+"/whitelist"),
            "channels_list": helpers.db_get(db, self.root+"/channels_list", is_list=True),
            "autoban_list": helpers.db_get(db, self.root+"/autoban_list", is_list=True),
            "suggestions_channels": helpers.db_get(db, self.root+"/suggestions_channels", is_list=True),
            "nomoney_channels": helpers.db_get(db, self.root+"/nomoney_channels", is_list=True),
            "auto_level_roles": helpers.db_get(db, self.root+"/auto_level_roles", is_list=True),
            "whitelist_ids": helpers.db_get(db, self.root+"/whitelist_ids", is_list=True),
            "welcome_channel": helpers.db_get(db, self.root+"/welcome_channel"),
            "general_channel": helpers.db_get(db, self.root+"/general_channel"),
            "rules_channel": helpers.db_get(db, self.root+"/rules_channel"),
            "logs_channel": helpers.db_get(db, self.root+"/logs_channel"),
            "polls_channel": helpers.db_get(db, self.root+"/polls_channel"),
            "math_channel": helpers.db_get(db, self.root+"/math_channel"),
            "casino_channel": helpers.db_get(db, self.root+"/casino_channel"),
            "everyone_role": helpers.db_get(db, self.root+"/everyone_role"),
            "goon_role": helpers.db_get(db, self.root+"/goon_role"),
            "mod_role": helpers.db_get(db, self.root+"/mod_role"),
            "roles_shop_id": helpers.db_get(db, self.root+"/roles_shop_id"),
            "roles_exclusive_id": helpers.db_get(db, self.root+"/roles_exclusive_id"),
            "counting_channel": helpers.db_get(db, self.root+"/counting_channel")
        }
        self.restrictions = {
            "whitelist": [helpers.is_bool, "0, 1"],
            "autofilter_trigger": [helpers.is_int, "Integer"],
            "is_locked_channels": [helpers.is_bool, "0, 1"],
            "is_locked_server": [helpers.is_bool, "0, 1"],
            "newaccounts_age": [helpers.is_int, "Integer"],
            "channels_list": [helpers.is_pos, "Positive integer"],
            "auto_level_roles": [helpers.is_pos, "Positive integer"],
            "suggestions_channels": [helpers.is_pos, "Positive integer"],
            "nomoney_channels": [helpers.is_pos, "Positive integer"],
            "whitelist_ids": [helpers.is_pos, "Positive integer"],
            "welcome_channel": [helpers.is_pos, "Positive integer"],
            "general_channel": [helpers.is_pos, "Positive integer"],
            "rules_channel": [helpers.is_pos, "Positive integer"],
            "polls_channel": [helpers.is_pos, "Positive integer"],
            "math_channel": [helpers.is_pos, "Positive integer"],
            "casino_channel": [helpers.is_pos, "Positive integer"],
            "everyone_role": [helpers.is_pos, "Positive integer"],
            "goon_role": [helpers.is_pos, "Positive integer"],
            "mod_role": [helpers.is_pos, "Positive integer"],
            "roles_shop_id": [helpers.is_pos, "Positive integer"],
            "roles_exclusive_id": [helpers.is_pos, "Positive integer"],
            "counting_channel": [helpers.is_pos, "Positive integer"]
        }

    def get(self, setting):
        if setting in self.settings:
            return self.settings[setting]
        else:
            raise Exception("That setting doesn't exist")

    def set(self, setting, val):
        val = int(val)
        if setting in self.settings:
            if type(self.settings[setting]) is list:
                raise Exception("Use add/remove to edit lists")
            if setting in self.restrictions:
                if not self.restrictions[setting][0](val):
                    raise Exception("That is an invalid setting: " + str(self.restrictions[setting][1]))
            self.settings[setting] = helpers.db_set(self.db, self.root+"/"+setting, val)
        else:
            raise Exception("That setting doesn't exist")

    def add(self, lname, val):
        val = str(val)
        if lname in self.settings:
            if not type(self.settings[lname]) is list:
                raise Exception("Argument is not a list")
            if lname in self.restrictions:
                if not self.restrictions[lname][0](val):
                    raise Exception("That is an invalid setting: " + str(self.restrictions[lname][1]))
            self.settings[lname].append(helpers.db_add(self.db, self.root+"/"+lname, val))
        else:
            raise Exception("That setting doesn't exist")

    def remove(self, lname, index):
        lname = str(lname)
        index = int(index)
        if lname in self.settings:
            if not type(self.settings[lname]) is list:
                raise Exception("Argument is not a list")
            self.settings[lname].remove(helpers.db_remove(self.db, self.root+"/"+lname, self.settings[lname], index))
        else:
            raise Exception("That setting doesn't exist")