from mvnScrapper import MVNscrapper
import os

#root = "https://mvnrepository.com/artifact/org.picketbox/picketbox/5.1.0.Final"
#root = "https://mvnrepository.com/artifact/org.springframework.security/spring-security-core/5.2.0.RELEASE"
max_depth = 4
root = "https://mvnrepository.com/artifact/org.acegisecurity/acegi-security/1.0.7"

path = os.getcwd().replace('\\', '/') + "/test_files"

f_dir = path+"/mvn_scrapper"
p_dir = path+"/scrap_management"

mvn_scrapper = MVNscrapper(root, max_depth, f_dir, p_dir)
input()