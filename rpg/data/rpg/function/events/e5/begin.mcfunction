scoreboard players set #ev rpg_ev 5
scoreboard players operation #end rpg_ev = #now rpg_ev
scoreboard players add #end rpg_ev 1200
data modify storage rpg:events cur.n set value "空缺者显现"
execute store result storage rpg:events cur.x int 1 run data get entity @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] Pos[0]
execute store result storage rpg:events cur.z int 1 run data get entity @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] Pos[2]
