# YoudaoDictpen_db_fix
临时用，尝试修复在未登录下无法访问好题本清单的情况

## 食用方法
1.下载dbfix.exe<br>
2.将词典笔连上电脑，并打开adb调试<br>
3.登录adb并提取db文件<br>
```
adb shell auth
adb pull /userdisk/math/exerciseFav/exerciseFavorite.db exerciseFavorite.db
```
4.打开dbfix.exe，选择刚刚提取出的db文件，然后点击"Execute Operation"按钮<br>
5.然后将修改完的文件push回去
```
adb push exerciseFavorite.db /userdisk/math/exerciseFav/exerciseFavorite.db
```
6.完成<br><br>

当然，你也可以观看 教程.mp4
