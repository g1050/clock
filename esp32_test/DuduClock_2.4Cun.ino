#include <Preferences.h>
#include <HTTPClient.h> // HTTP通信库
#include <WiFi.h> //wifi网络库
#include <WebServer.h> // web服务器
#include <ArduinoJson.h> // 解析json的库

#define D4 12  // 开发板D4灯

String ssid;  //WIFI名称
String pass;  //WIFI密码
String city;  // 城市

void setWiFiCity(String ssid,String pass,String city){
  prefs.begin("clock");
  prefs.putString("ssid", ssid);
  prefs.putString("pass", pass);
  prefs.putString("city", city);
  prefs.end();
}

void getWiFiCity(){
  prefs.begin("clock");
  ssid = prefs.getString("ssid", "");
  pass = prefs.getString("pass", "");
  city = prefs.getString("city", "");
  prefs.end();
}

void restartSystem(String msg, bool endTips){
  if(endTips){
    //结束循环显示提示文字的定时器
    timerEnd(timerShowTips);
  }
  // reflashTFT();
  for(int i = 3; i > 0; i--){
    String text = "";
    text = text + i + "秒后系统重启";
    // draw2LineText(msg,text);
    delay(1000);
  }
  ESP.restart();
}

void connectWiFi(int timeOut_s){
  delay(1500); // 让“系统启动中”字样多显示一会
  // drawText("正在连接网络...");
  int connectTime = 0; //用于连接计时，如果长时间连接不成功，复位设备
  pinMode(D4,OUTPUT); // 将D4引脚设置为输出模式。为了控制连接状态的指示灯
  Serial.print("正在连接网络");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    digitalWrite(D4, !digitalRead(D4));
    delay(500);
    connectTime++;
    if (connectTime > 2 * timeOut_s){ //长时间连接不上，清除nvs中保存的网络数据，并重启系统
      Serial.println("网络连接失败,即将重新开始配置网络...");
      clearWiFiCity();
      restartSystem("网络连接失败", false);
    }
  }
  digitalWrite(D4, LOW); // 连接成功后，将D4指示灯熄灭
  Serial.println("网络连接成功");
  Serial.print("本地IP： ");
  Serial.println(WiFi.localIP());
}

void clearWiFiCity(){
  prefs.begin("clock");
  prefs.remove("ssid");
  prefs.remove("pass");
  prefs.remove("city");
  prefs.remove("backColor");
  prefs.end();
}

void startServer(){
  // 当浏览器请求服务器根目录(网站首页)时调用自定义函数handleRoot处理，设置主页回调函数，必须添加第二个参数HTTP_GET，否则无法强制门户
  server.on("/", HTTP_GET, handleRoot);
  // 当浏览器请求服务器/configwifi(表单字段)目录时调用自定义函数handleConfigWifi处理
  // server.on("/configwifi", HTTP_POST, handleConfigWifi);
  // 当浏览器请求的网络资源无法在服务器找到时调用自定义函数handleNotFound处理   
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("服务器启动成功！");
}

// void handleRoot(){
//   server.send(200,"text/html", ROOT_HTML_PAGE1 + WifiNames + ROOT_HTML_PAGE2);
// }

void handleRoot() {
  // 创建一个 DynamicJsonDocument 对象，你可以根据需要调整大小
  const size_t capacity = JSON_OBJECT_SIZE(1) + 20;  // 1个键值对，20是预估的字符串长度
  DynamicJsonDocument doc(capacity);
  // 向 JSON 对象中添加键值对
  doc["message"] = "ok";
  // 使用 JsonObject 生成 JSON 字符串
  String jsonString;
  serializeJson(doc, jsonString);
  // 发送 JSON 响应
  server.send(200, "application/json", jsonString);
}


void handleNotFound(){
  handleRoot();//
}

void setup() {
  Serial.begin(115200); 
  setWiFiCity("ssid","passwd","city");
  getWiFiCity();
  connectWiFi(30);
  startServer();
}
void loop() {
 
}

