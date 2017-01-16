svuregr = read.csv(file = "C:/Users/peteo/Documents/Pete/xG2_regression_data_12_16.csv", header = T)
install.packages("glmnet")
library(glmnet)
svuregr$angle_dist = svuregr$angle/svuregr$distancetogoal
svuregr$angle2 = svuregr$angle^2
svuregr$invangle2 = 1/svuregr$angle^2
svuregr$invangle = 1/svuregr$angle
svuregr$invdist = 1/svuregr$distancetogoal
svuregr$invdist2 = 1/svuregr$distancetogoal^2
svuregr$BigHead = svuregr$isBigChance*svuregr$shotHead

svuregr2 = svuregr[,c(2,9,11:15,17:28,30,35,36)]

x3<-model.matrix(isGoal~.,data=svuregr2)
x3=x3[,-1]

glmnet_conv<-cv.glmnet(x=x3,y=svuregr2$isGoal,
                       alpha=0,
                       family='binomial'
)

coef(glmnet_conv, s= glmnet_conv$lambda.min)
plot(glmnet_conv)     

exp(predict.cv.glmnet(glmnet_conv, newx=x3, s=glmnet_conv$lambda.min))/(1+exp(predict.cv.glmnet(glmnet_conv, newx=x3, s=glmnet_conv$lambda.min))) -> probs

summary(probs)
summary(svuregr2$angle)


######################

svuregr3 = svuregr[,-c(1,3:8,10)]

xg3<-model.matrix(isGoal~.,data=svuregr3)
xg3=xg3[,-1]

glmnet_conv2<-cv.glmnet(x=xg3,y=svuregr3$isGoal,
                       alpha=1,
                       family='binomial'
)

coef(glmnet_conv2, s= glmnet_conv2$lambda.min)
plot(glmnet_conv2)     

exp(predict.cv.glmnet(glmnet_conv, newx=x3, s=glmnet_conv$lambda.min))/(1+exp(predict.cv.glmnet(glmnet_conv, newx=x3, s=glmnet_conv$lambda.min))) -> probs

summary(probs)
summary(svuregr2$angle)


cuts <- cut(svuregr3$goalmouthY, c(-Inf,seq(45.2, 54.8, 1.6), Inf), labels=0:7)

cuts <- as.data.frame(cuts)

summary(cuts)
summary(svuregr3$goalmouthY[which(svuregr3$isGoal==1)])

summary(cuts$cuts)



summary(svuregr3$goalmouthZ)

cuts2 <- cut(svuregr3$goalmouthZ, c(-Inf,seq(0, 38, 9.5), Inf), labels=c('a','b','c','d','e','f'))
cuts2 <- as.data.frame(cuts2)

summary(cuts2)
summary(svuregr3$goalmouthY[which(svuregr3$isGoal==1)])

summary(cuts2$cuts)
