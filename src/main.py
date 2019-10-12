from mvnScrapper import MVNscrapper

#root = "https://mvnrepository.com/artifact/org.springframework.security/spring-security-web"
#version = "/5.1.6.RELEASE"
root = "https://mvnrepository.com/artifact/org.apache.shiro/shiro-web/1.4.1"
max_depth = 3

f_dir = "E:/1. Caio Shimada/TCC/test_files/mvn_scrapper"
p_dir = "E:/1. Caio Shimada/TCC/test_files/scrap_management"

mvn_scrapper = MVNscrapper(root, max_depth, f_dir, p_dir)
input()
