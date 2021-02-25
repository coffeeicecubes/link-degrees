#standard lib
import sys

#libraries to get web page response and parse the html
import requests
from bs4 import BeautifulSoup

#TODO Add inheritance/weights?

# change recursion limit for large searches like through wikipedia
sys.setrecursionlimit(50)

log = open('log.txt', 'w+')

#this is a node with a link and a parent link
class Page:
    def __init__(self, link, parent):
        self.link = link
        self.parent = parent

    #specify how to print the node/convert it to a string
    def __str__(self):
        return self.link
    def __repr__(self):
        return self.link

    #get all valid links on the page (valid meaning that they belong to the same website/2-3 levels of domain name)
    def getHrefs(self):
        l = []
        resp = requests.get(self.link)
        #make sure that the link is valid
        if resp.status_code != 200:
            return []

        #setup parser
        soup = BeautifulSoup(resp.text,'lxml')
        #get all link text (href val)
        for x in soup.findAll('a'):
            href = x.get('href')
            try:
                #starting with a slash means the referenced page is in a sub-folder/current folder
                #starting with ./ means it is in the above folder
                if href[0] == '/':
                    l.append(HL_DOMAIN + href)
                elif href[:2] == './':
                    l.append(HL_DOMAIN + href[1:])

            except:
                continue
        return l

#a queue data-structure (LIFO - last in first out)
class Q:
    def __init__(self):
        self.q = []
    
    def __str__(self):
        return str(self.q)

    def isEmpty(self):
        if not self.q:
            return True
        return False
    
    #is a page identified by a certain link in the queue?
    def contains(self, y):
        for x in self.q:
            if x.link == y:
                return True
        return False

    #adds node to 'end' of queue
    def add(self, page):
        self.q.append(page)

    #gets next node (from 'front') and removes it from the queue
    def next(self):
        if not self.isEmpty():
            return self.q.pop(0)
        else:
            return False

#stack data structure (FIFO - first in first out)
class Stack:
    def __init__(self):
        self.sset = []

    def __str__(self):
        return repr([repr(x) for x in self.sset])

    #add a node to the 'top' of the stack if its not already there
    def push(self, page):
        if page not in self.sset:
            self.sset.append(page)

    #remove a node from the 'top' of the stack (if stack not empty)
    def pop(self):
        if self.sset:
            self.sset.pop(0)
        else:
            return False

    def contains(self, y):
        for x in self.sset:
            if x.link == y:
                return True
        return False

    #returns dict mapping each link to its parent
    def toDict(self):
        d = {}
        for page in self.sset:
            d[page.link] = page.parent
        return d

#breadth first search!
#q = unvisited, a queue, keeps track of next nodes to visit
#sset = solution set/visisted nodes
#rl = current recursion level - useful for debugging
def bfs(q, sset, target, rl=0):
    log.write(f"Recursion level: {rl}\n")
    rl += 1
    log.write(f"Current queue: {q}\n")

    #get next node to process ('current') and remove it from the queue
    cur = q.next()

    #if the queue is empty, the node will be 'False'. Empty queue means no solution, so return now
    if not cur:
        return False
    
    log.write(f"Queue after removal: {q}\n")
    log.write(f"Current link: {cur}\n")
    
    #make sure that you dont visit the same link twice bc that's useless and a waste of time and won't find you the shortest route
    if not sset.contains(cur.link):
        #get all links that are referenced by the current one
        links = cur.getHrefs()

        log.write(f"Links in current url are {links}\n")

        #check if target node in links (on current page)
        if target in links:
            log.write(f"TARGET FOUND\n\n")
            #if the target link is present, add its parent to the 'visited' queue and return
            sset.push(cur)
            return sset, Page(target, cur)

        #ensure that there are valid links in the list, and if so, add each to the queue (as a Page, saving the parent) to be later processed
        if links:
            log.write(f"{cur} marked as visited\n")

            #add the current node to 'visited' stack
            sset.push(cur)
            for x in links:
                y = Page(x, cur.link)
                log.write(f"New page created: {y}\n")

                if not q.contains(y.link):
                    log.write(f"Adding {y} to the queue\n")
                    q.add(y)
                else:
                    log.write("We have already come across this link\n")
        else:
            log.write("No [valid] links on page\n")
    log.write(f"Current solution set: {sset}\n\n\n")

    #recurse until the function returns (either because it found the node or because it cannot)
    return bfs(q, sset, target, rl)

#map the link structure out (associate the target link to all of the proceeding parent links)
def map(sset, target_node):
    sset = sset.toDict() #[returns dict mapping each link to its parent]
    s = []
    s.append(target_node.parent)

    #it was infuriating to figure out that accessing the 'parent' link of a node doesn't properly return a string, causing a 'KeyError' even though the key exists
    cur = sset[f"{target_node.parent}"]
    while cur:
        s.append(cur)
        cur = sset[cur]

    #reversal since you are mapping backwards through parents
    s.reverse()

    #add the target to the end of the list (its the end goal node)
    s.append(target_node.link)
    return s

#get source and target + infer hl_domain from user if you want (not recommended)
"""
def getUserInp():
    source = input("First link: ")
    if 'https://' not in source:
        source = 'https://' + source

    try:
        hl_domain = source.split('/')[2]
        print(hl_domain)
    except:
        print('url format is incorrect')
        sys.exit(-1)

    dest = input("Second link (same domain): ")
    if 'https://' not in source:
        dest = 'https://' + dest

    if hl_domain not in dest:
        print('same domain!')
        sys.exit(-1)
    if source == dest:
        print('source and dest cannot be the same!')
        sys.exit(-1)
    return source, dest, hl_domain
"""

#setup everything
def main():
    orig = Page(source, False)

    q = Q()
    q.add(orig)

    sset = Stack()
    try:
        sset, target_node = bfs(q, sset, target)
    except TypeError:
        print('No connection found')
        sys.exit()
    
    print(f"Connection found from {source} to {target} through: ")
    sset = map(sset, target_node)

    print(sset)
    print("complete!")


if __name__ == "__main__":
    #run python3 -m http.server 9999 IN THIS FOLDER and click on www/ and then p1.html - localhost testing server with some linked together html pages

    #hardcoded
    source = "http://localhost:9999/www/p1.html"
    target = "http://localhost:9999/www/p8.html"
    HL_DOMAIN = "http://localhost:9999/www"
    
    main()
    #remember to close files! (best practice is with('x.txt', 'w+') as f: which automatically closes, but this way is more readable and just as effective)
    log.close()
    
    #bye!
    sys.exit(1)
