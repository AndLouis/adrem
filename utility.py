import csv
import os.path
from pathlib import Path

files_1 = os.path.join(os.path.dirname(__file__), 'utility_files/cp_ALLEGATO_01_eng.csv')
files_2 = os.path.join(os.path.dirname(__file__), 'utility_files/cp_ALLEGATO_02_eng.csv')

class myCSV:
    def __init__(self,path,delimiter):
        self.path = self.ispath(path)
        if delimiter == 'space':
            delimiter_ = ' '
        else:
            delimiter_ = delimiter
        with open(self.path, newline='') as f:
            self.thecsv = list(csv.reader(f,delimiter=delimiter_))
        self.header = self.getheader()
        self.key_value = self.makedict()


    def ispath(self, path):
        if not os.path.isfile(path):
            raise Exception("can't find {}".format(path))
        else:
            return path

    def getheader(self):
        return self.thecsv[0]

    def makedict(self):
        ret = []
        keys = self.getheader()
        for each in self.thecsv[1:]:
            tmp = {}
            for i in range(len(each)):
                try:
                    tmp[keys[i]] = each[i]
                except IndexError:
                    pass
            ret.append(tmp)
        return ret

    def getbykeyvalue(self, key, value):
        if key not in self.header:
            raise Exception("key {} doesnt exist".format(key))
        for el in self.key_value:
            if el[key] == value:
                return el
        raise Exception('value {} doesnt exist'.format(value))


class Allegato_first:
    def __init__(self):
        with open(files_1, newline='') as f:
            self.thecsv = list(csv.reader(f,delimiter=";"))
        self._res_l, self._ind_l = self.make_limit()

    def make_limit(self):
        res_l = {}
        ind_l = {}
        for each in self.thecsv:
            res_l[each[0]] = each[1]
            ind_l[each[0]] = each[2]
        return res_l, ind_l

    def _get_lim_res(self, key):
        return self._res_l[key]
    def _get_lim_ind(self, key):
        return self._ind_l[key]

class Allegato_second:
    def __init__(self):
        with open(files_2, newline='') as f:
            self.thecsv = list(csv.reader(f,delimiter=";"))
        self._l= self.make_limit()

    def make_limit(self):
        ret = {}
        for each in self.thecsv:
            ret[each[0]] = each[1]
        return ret

    def _get_lim(self, key):
        return self._l[key]

    
    

