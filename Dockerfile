FROM openjdk:21
EXPOSE 8080
ADD target/EvaSupportAgent-0.0.1-SNAPSHOT.jar EvaSupportAgent-0.0.1-SNAPSHOT.jar
ENTRYPOINT ["java","-jar","/EvaSupportAgent-0.0.1-SNAPSHOT.jar"]