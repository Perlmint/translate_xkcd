var list = ["149","1077","1098","1123","1137","1168","1174","1180","1184","1195","1197","1200","1381","1403","1411","1441","1444","1445","1448","1495"];var getRandomID = function() {return list[Math.floor(Math.random() * list.length)];};var gotoRandomPage = function() {location.href = "./" + getRandomID() + "/index.html";};