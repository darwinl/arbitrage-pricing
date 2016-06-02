import requests

class Node(object):
    def __init__(self, currency, weight=1.0):
        self.currency = currency
        self.weight = weight
        self.children = {}

    def add_child(self,node):
        self.children[node.currency] = node

    def arbitrage_route(self, matrix):

        if not self.children:
            return [self.currency]

        maxweight = 0.0
        list = []
        for fx, child in self.children.items():
            route = child.arbitrage_route(matrix)
            weight = matrix.arbitrage_weight(self.currency, route)
            if weight > maxweight:
                maxweight = weight
                list = route

        return [self.currency] + list

class Matrix(object):
    def __init__(self):
        self.matrix = {}

    def add(self,fromfx,tofx,value):
        if fromfx not in self.matrix:
            self.matrix[fromfx] = {}
        self.matrix[fromfx][tofx] = value

    def get(self,fromfx,tofx):
        return self.matrix[fromfx][tofx]

    def fromfxs(self):
        return self.matrix.keys()

    def tofxs(self,fromfx):
        return self.matrix[fromfx].keys()

    def arbitrage_weight(self, fromfx, list):

        weight = 1.0

        if len(list) > 1:
            for num in xrange(0,len(list)-1):
                weight = weight * self.matrix[list[num]][list[num+1]]

        if fromfx == "":
            return weight

        return self.matrix[fromfx][list[0]] * weight


class Ancestors(object):

    def __init__(self):
        self.list = []
        self.dict = {}
        self.root = None

    def push(self,currency):
        if self.root is None:
            self.root = currency
        self.list.append(currency)
        self.dict[currency] = currency

    def has(self,currency):
        return currency in self.list

    def pop(self):
        currency = self.list.pop()
        self.dict.pop(currency)


class Tree(object):

    def __init__(self,root,matrix):
        self.root = root
        self.matrix = matrix
        self.__tree = self.__internal_tree(self.root)

    def __internal_tree(self,node,ancestors=None):

        if not ancestors:
            ancestors = Ancestors()

        # push node to ancestors
        fromfx = node.currency
        ancestors.push(fromfx)

        for childfx in self.matrix.tofxs(fromfx):
            if childfx == fromfx:
                continue
            if childfx == self.root.currency:
                node.add_child(Node(childfx, self.matrix.get(fromfx, childfx)))
            elif not ancestors.has(childfx):
                childnode = Node(childfx, self.matrix.get(fromfx, childfx))
                childnode = self.__internal_tree(childnode,ancestors)
                node.add_child(childnode)

        ancestors.pop()
        return node

    def arbitrage_route(self):
        return self.root.arbitrage_route(self.matrix)

url = "http://fx.priceonomics.com/v1/rates/"
resp = requests.get(url=url)
data = resp.json()

#data = {"USD_JPY": "116.3270016", "USD_USD": "1.0000000", "JPY_EUR": "0.0065592",
#        "BTC_USD": "124.5494571", "JPY_BTC": "0.0000701", "USD_EUR": "0.8831901",
#        "EUR_USD": "1.2408685", "EUR_JPY": "127.1369502", "JPY_USD": "0.0084318",
#        "BTC_BTC": "1.0000000", "EUR_BTC": "0.0108640", "BTC_JPY": "12749.6564478",
#        "JPY_JPY": "1.0000000", "BTC_EUR": "91.8708418", "EUR_EUR": "1.0000000",
#        "USD_BTC": "0.0094256"}

# json = {"USD_JPY": "115.5967961", "USD_USD": "1.0000000", "JPY_EUR": "0.0066133", "BTC_USD": "127.0783836", "JPY_BTC": "0.0000706", "USD_EUR": "0.8776462", "EUR_USD": "1.2138793", "EUR_JPY": "124.3716902", "JPY_USD": "0.0085014", "BTC_BTC": "1.0000000", "EUR_BTC": "0.0106277", "BTC_JPY": "13008.5330759", "JPY_JPY": "1.0000000", "BTC_EUR": "93.7362422", "EUR_EUR": "1.0000000", "USD_BTC": "0.0093664"}

m = Matrix()

for key in sorted(data.keys()):
    route = key.split('_')
    fromfx = route[0]
    tofx = route[1]
    m.add(fromfx,tofx,float(data[key]))


maxweight = 0.0
maxroute = []
for fromfx in m.fromfxs():
    node = Node(fromfx)
    tree = Tree(node,m)
    route = tree.arbitrage_route()
    weight = m.arbitrage_weight("", route)
    if (weight > maxweight):
        maxweight = weight
        maxroute = route

print maxweight
print maxroute








