# 圣卫全倒（as 载体）：命令没人执行了，6 秒破绽，之后重新授权
tag @s remove rpg.usb.guarded
tag @s add rpg.usb.reauth
scoreboard players set @s rpg_ub_x 120
function rpg:usurper_boss/weak/start
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#F0CF7A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"有权无力 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"……没有人执行我的命令？","color":"#9C9A94","bold":false,"italic":false}]
