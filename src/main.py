from MVNScrapper import MVNScrapper
from UI import Home
from tkinter import Tk
import os

if __name__ == '__main__':
    root = Tk()
    deps = Home(root)
    root.mainloop()

# max_depth = 4
# root = "https://mvnrepository.com/artifact/org.springframework.security/spring-security-core/5.2.0.RELEASE"
# root = 'https://mvnrepository.com/artifact/org.apache.shiro/shiro-core/1.4.1'
# root = "https://mvnrepository.com/artifact/org.picketbox/picketbox/5.1.0.Final"
# root = "https://mvnrepository.com/artifact/org.acegisecurity/acegi-security/1.0.7"

# path = os.getcwd().replace('\\', '/') + "/test_files"

# f_dir = path+"/mvn_scrapper"
# p_dir = path+"/scrap_management"

# scrapper = MVNScrapper()
# scrapper.scrap(root, max_depth, f_dir, p_dir)
