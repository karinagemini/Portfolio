
getwd()


# install.packages("readxl")
library(readxl)
library(ggplot2)

v1 <- read_excel("4 th year/Computational Social Science/results/Top10_Canada.xlsx")
v1$keywords <- ordered(v1$keywords,levels=v1$keywords)


v2 <- read_excel("4 th year/Computational Social Science/results/v2_melted_Canadadeveloper.xlsx")
v2 $Keyword <- ordered(v2$Keyword,levels=unique(v2$Keyword))
v2 $Group <- factor(v2$Group)

v3 <- read_excel("4 th year/Computational Social Science/results/v3_melted_Canadamanager.xlsx")
v3 $Keyword <- ordered(v3$Keyword,levels=unique(v3$Keyword))
v3 $Group <- factor(v3$Group)




# Plot Top 10 Keyword Frequencies
p<-ggplot(dat=v1,aes(x=keywords,y=counts))+
  geom_bar(stat="identity")+
  scale_x_discrete(guide = guide_axis(angle = 45)) +
  ggtitle("Economic Group's Top 10 Keyword Frequencies for Canada")
p

ggsave("top10_Canada.png",plot = p,height=110,width=200,units="mm",dpi = 500)


# Plot Top 10 Keyword Frequencies, two types ("Developer")
p<-ggplot(dat=v2,aes(x=Keyword,y=Frequency,fill=Group))+
  geom_bar(stat="identity",position=position_dodge())+
  scale_x_discrete(guide = guide_axis(angle = 45)) +
  ggtitle("Economic Group's Top 10 Keyword Frequencies for Canada, Two Types, Developer")
p

ggsave("top10_2types_CanadaDeveloper.png",plot = p,height=110,width=200,units="mm",dpi = 500)


# Plot Top 10 Keyword Frequencies, two types ("Manager")
p<-ggplot(dat=v3,aes(x=Keyword,y=Frequency,fill=Group))+
  geom_bar(stat="identity",position=position_dodge())+
  scale_x_discrete(guide = guide_axis(angle = 45)) +
  ggtitle("Economic Group's Top 10 Keyword Frequencies for Canada, Two Types, Manager")
p

ggsave("top10_2types_CanadaManager.png",plot = p,height=110,width=200,units="mm",dpi = 500)



