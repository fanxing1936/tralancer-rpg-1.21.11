# 请求建一座镇（宏 i）：还没动过就排进队列
$execute if score #s$(i) rpg_tw matches 0 run scoreboard players set #s$(i) rpg_tw 1
