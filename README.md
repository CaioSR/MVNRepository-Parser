Deps Ahoy is an extracting tool used on MVNRepository to extract dependencies graphs.

Requires Requests and BeautifulSoup.

--pip install requests

--pip install beautifulsoup4

Note: In December 2019, Python 3.8.x had a memory leak while using beautifulsoup4. For this reason
Python 3.7.x was needed. I don't know if this issue has been fixed, but keep this in mind.

This generates two main files: Nodes.csv and Links.csv. But also generates a ton of other files (for now) to avoid losing progress in case an interruption occurs.

The extraction time is long due to an access limitation on the website.

All that is needed to start an extraction is an url of the maven artifact in a specific version, 
how deep the tool should go to extract and the location of the files to write.

This does not construct the Graph, it only creates the files. For the visualization you can use Gephi, but you must execute the Add Ids on the UI before importing the files to the software.