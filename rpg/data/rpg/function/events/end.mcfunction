# 事件结束（超时或完成）
execute if score #ev rpg_ev matches 1 run function rpg:events/e1/stop
execute if score #ev rpg_ev matches 2 run function rpg:events/e2/stop
execute if score #ev rpg_ev matches 3 run function rpg:events/e3/stop
execute if score #ev rpg_ev matches 4 run function rpg:events/e4/stop
execute if score #ev rpg_ev matches 5 run function rpg:events/e5/stop
execute if score #ev rpg_ev matches 6 run function rpg:merchant/ev/stop
scoreboard players set #ev rpg_ev 0
data modify storage rpg:events cur.n set value ""
kill @e[type=minecraft:marker,tag=rpg.ev.mk]
