import os
import random
import re
import sys



# need for random number
b = random.SystemRandom()

DAMPING = 0.85
SAMPLES = 100000

def percentage(n):
    a = b.randrange(0,100)
    if a < n:
        return a
    return False

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    #print(sum(ranks.values()))

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    #print(sum(ranks.values()))
def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, currentPage, dampingFactor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    retVal = {}

    for newPage in corpus[currentPage]:
        if percentage(dampingFactor):
            if newPage in retVal:
                retVal[newPage] += 1
            else:
                retVal[newPage] = 1

    if percentage(dampingFactor):
        randomPage = random.choice(list(corpus.keys()))
        if randomPage in retVal:
            retVal[randomPage] += 1
        else:
            retVal[randomPage] = 1


    totalClicks = 0
    for k,v in retVal.items():
        totalClicks+=v
    
    for k,v in retVal.items():
        temp = round(((v * 1000) / totalClicks) / 1000,4)
        retVal[k] = temp

    return retVal


def sample_pagerank(corpus, dampingFactor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dampingFactor = dampingFactor * 100
    pageCount = 0
    pageRank = {}
    for key in corpus.keys():
        pageRank[key] = 0
        pageCount += 1

    nextPage = random.choice(list(corpus.keys()))
    for i in range(n):
        currentProbability = transition_model(corpus,nextPage,dampingFactor)
        for k,v in currentProbability.items():
            if percentage(v * 100):
                pageRank[k] += v

        moves = {}
        pickRandomPage = True
        for i in currentProbability.keys():
            temp = percentage(dampingFactor)
            if temp:
                moves[i] = temp
                pickRandomPage = False
        
        if not pickRandomPage:
            best = 0
            for i in moves:
                if moves[i] > best:
                    best = moves[i]
                    nextPage = i

        if pickRandomPage:
            nextPage = None
            while not nextPage:
                for i in corpus.keys():
                    if percentage(dampingFactor):
                        nextPage = i
                        break
            
    
    totalValues = 0
    for k,v in pageRank.items():
        totalValues += v
    
    for k,v in pageRank.items():
        v = v * 1000
        pageRank[k] = round((v / totalValues) / 1000,4)
    return pageRank


def iterate_pagerank(corpus, damping_factor):
    LinksToMe = {}
    for key in corpus.keys():
        pagesLinkingToMe = set()
        for k,v in corpus.items():
            if k == key:
                continue
            for i in v:
                if i == key:
                    pagesLinkingToMe.add(k)
        LinksToMe[key] = pagesLinkingToMe
    d = {}

    pageLinks = {}
    for k,v in corpus.items():
        vlen = len(v)
        pageLinks[k] = vlen
    
    someConstant = (1 - damping_factor) / len(corpus)
    for k in corpus.keys():
        d[k] = 1.0 / len(corpus)
    
    oldValues = {}
    while True:
        for i in d:
            oldValues[i] = d[i]
        for k in corpus.keys():
            v = LinksToMe[k]
            linkingPageSum = 0
            for i in v:
                PR_i = d[i]
                linkingPageSum += (((PR_i * 100000) / pageLinks[i]) / 100000)
            # If no pages link to a page, it must receive the lowest possible page ranking at this time, excluding itself
            if len(v) == 0:
                total = 0
                for newKey,newValue in d.items():
                    if newKey != k:
                        total += newValue
                d[k] = 1 - total
            else:
                d[k] = (someConstant + (damping_factor * linkingPageSum))
        numConvergent = 0
        for i in d.keys():
            a = d[i]
            b = oldValues[i]
            # When convergence occurs at 0.0001, it's more accurate than convergence at 0.001.
            # However, the problem specifications do not say to stop at 0.0001, so I will not do that. I am sad.
            if abs(a - b) < 0.001:
                numConvergent += 1
            if numConvergent >= len(d):
                return d
    return d


if __name__ == "__main__":
    main()
