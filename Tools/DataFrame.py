
class DataFrameTools:

    def __init__(self):
        pass

    def remove_building_equip_text(self, display_name_string):
        """
        Splits the string on "-" and returns the first match.  Effective in removing the "-buildingEquip" text
        from a string.
        :param display_name_string: Display Name ('dis')
        :return: Display Name with the "-buildingEquip" removed
        """
        if "-" in display_name_string:
            return display_name_string.split("-")[0]
        else:
            return display_name_string

    def remove_type_infromation_text(self, type_text):
        """
        Removes the type text from an entry.  This text usually appears as "n:", or something similar.
        :param type_text: Information returned from 75F API
        :return: Information without the type text.
        """
        if ":" in type_text:
            return type_text.split(":")[1]
        else:
            return type_text


    def get_float_from_string(self, float_text):
        """
        Retrieves the floating point number portion of a string.  Only one floating point number is returned.
        :param float_text: Text with floating point number in it
        :return: floating point number
        """
        # Regular Expression (Regex) pattern to recognize floating point values surrounded by text.
        # This code assumes there is only one numeric value in the text.
        float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
        match = re.search(float_pattern, float_text)
        if match:
            return float(match.group())
        else:
            # raise Exception(f"Cannot convert to float: {float_text}")
            return float(-998.0)