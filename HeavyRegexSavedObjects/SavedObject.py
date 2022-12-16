import re


class SavedObject(object):
    def __init__(self, raw_json, references, full_id):
        self.raw_json = raw_json
        self.name = self.raw_json.get("title")
        self.object_id = self.get_id(full_id)
        self.panel_json = self.raw_json.get("panelsJSON")
        self.references = references
        self.company = self.get_company()
        self.last_updated = self.raw_json.get("_updatedAt")

    def get_index(self):
        """
        Relevant only for Visualizations and Searches.
        :return: set of index names used by Object.
        """
        index = None
        indexes = []
        for obj in self.references:
            index = obj.get("id")[:-2]  # [:-2] is cutting the '-*' from the index end

            if index.startswith("["):  # supporting index format '[logz-<<RANDOM>>-]YYMMDD'
                index = index[1:-5]

            indexes.append(index)

        if len(indexes) > 1:
            index = indexes.pop()
        return index

    def get_company(self):
        """
        Returning the name of company that created the saved object.
        If it's an OOTB content, company name would be Logz.io.
        :return: the name of company that created the saved object.
        """
        if "_logzioProperties" in self.raw_json or "_logzioOriginalAppId" in self.raw_json:
            return "Logz.io"

        company = None
        pattern = re.compile("@(?P<company>.*?)\.\w+$")

        try:
            username = self.raw_json.get("_updatedBy").get("username")
            company = pattern.search(username).group("company")

        except AttributeError:
            print(f"Failed to find company at {self.raw_json}.")
        except TypeError:
            print(f"Failed to find company at {self.raw_json}, missing username.")

        return company

    def get_id(self, full_id):
        """
        Finding the ID of the saved object.
        :param full_id: the full id including the objec type (fron the raw object's JSON)
        :return: id of the saved object.
        """
        object_id = None
        pattern = re.compile("^\w+:(?P<object_id>.*)")

        try:
            object_id = pattern.search(full_id).group("object_id")

        except AttributeError:
            print(f"Failed to find id of {full_id}.")
        except TypeError:
            print(f"Failed to find id of {full_id}, missing full_id.")
        except Exception as e:
            print(f"Failed to find id of {full_id}, duo to unexpected error {e}.")

        if object_id:
            return object_id
        return full_id


class Dashboard(SavedObject):
    def __init__(self, raw_json, references, full_id, kibana_index):
        super().__init__(raw_json, references, full_id)
        self.visualizations_ids = self.get_visualizations_ids()
        self.index = self.get_index(kibana_index)  # calling it 'indexes' to keep field name same across classes

    def get_index(self, kibana_index):
        """
        Overloading of the parent method, finding the index prefix of account the dashboard exists in.
        :param kibana_index: the kibana index the dashboard came from.
        :return: the index prefix (logz-<<some_random_chars>>)
        """
        index = None
        pattern = re.compile("^kibana-(?P<index>.*?)-7")

        try:
            index = pattern.search(kibana_index).group("index")

        except AttributeError:
            print(f"Failed to find index of dashboard {self.name}.")
        except TypeError:
            print(f"Failed to find index of dashboard {self.name}, missing kibana_index.")
        except Exception as e:
            print(f"Failed to find index of dashboard {self.name} duo to unexpected error {e}.")

        return index

    def get_visualizations_ids(self):
        """
        returning the ID's of visualizations in the dashboard.
        :return: ids of the visualizations in the dashboard.
        """
        visualizations_ids = []
        for visualization in self.references:
            visualization_id = visualization.get("id")
            visualizations_ids.append(visualization_id)
        return visualizations_ids


class Visualization(SavedObject):
    def __init__(self, raw_json, references, full_id):
        super().__init__(raw_json, references, full_id)
        self.index = self.get_index()


class Search(SavedObject):
    def __init__(self, raw_json, references, full_id):
        super().__init__(raw_json, references, full_id)
        self.index = self.get_index()
