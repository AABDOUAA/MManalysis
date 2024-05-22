# this will be used to process and replace every node of the filtered_network
# to make the network more controllable

class networkNode:
    def __init__(self, value, name):
        self.value = value
        self.name = name
        self.uni, self.subLevel1, self.subLevel2 = self.findUni()
        # self.subLevel1 = self.findSubLevel1()
        # self.subLevel2 = self.findSubLevel2()

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def findUni(self):
        affiliationName = self.name
        splitName = affiliationName.split(',')
        search_strings = ["University", "College"]
        location = self.find_locations(splitName, search_strings)
        if location[0] == 0 and len(splitName) == 1:
            location2 = 0
            location3 = 0
        elif location[0] == 0:
            location2 = 1
            location3 = 1
        elif location[0] < 2:
          location2 = location[0] - 1
          location3 = location2
        else:
          location2 = location[0] - 1
          location3 = location2 - 1

        return splitName[location[0]].lstrip(), splitName[location2].lstrip(), splitName[location3].lstrip()

    def find_locations(self, elements, search_strings):
        locations = []
        index = 0
        for element in elements:
            #print(element)
            element = element.lower()
            for search_string in search_strings:
              search_string = search_string.lower()
              #print(search_string)
              if element.find(search_string) > 0:
                  locations.append(index)
                  #print('match')
                  break  # Stop searching further if any search string is found in the element
            index = index + 1
        if locations == []:
          locations = [0]
        return locations
