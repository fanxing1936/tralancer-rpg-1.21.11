scoreboard players set @s rpg_end_state 3
scoreboard players set @s rpg_end_time 0
scoreboard players add @s rpg_end_floor 1
scoreboard players operation #floor rpg_end_tmp = @s rpg_end_floor
bossbar set rpg:endless color purple
bossbar set rpg:endless name ["",{"text":"回廊重构｜下一层 ","color":"#C28BE0","bold":true,"italic":false},{"score":{"name":"#floor","objective":"rpg_end_tmp"},"color":"#FFF2A8","bold":true,"italic":false},{"text":"　6 秒","color":"dark_gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.end.member.current,distance=..96] ["",{"text":"[回廊重构] ","color":"#C28BE0","bold":true,"italic":false},{"text":"六秒后开启第 ","color":"#AAB4C3","bold":false,"italic":false},{"score":{"name":"#floor","objective":"rpg_end_tmp"},"color":"#FFF2A8","bold":true,"italic":false},{"text":" 层。","color":"#AAB4C3","bold":false,"italic":false}]
