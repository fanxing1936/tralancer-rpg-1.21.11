scoreboard players set #t rpg_pl 0
# 死在里面的人在主世界复活：要先接回来，这时维度里可能一个人都没有
execute as @a[tag=rpg.pl.in,scores={rpg_pl_dc=1..}] unless data entity @s {Dimension:"rpg:paradise_lost"} run function rpg:pl/revive
# 用别的办法离开了维度的人
execute as @a[tag=rpg.pl.in,scores={rpg_pl_dc=0}] unless data entity @s {Dimension:"rpg:paradise_lost"} run tag @s remove rpg.pl.in
execute in rpg:paradise_lost positioned 0 83 0 unless entity @a[distance=0..] run return 0
execute as @a[tag=rpg.pl.in,scores={rpg_pl_lv=1..}] at @s run function rpg:pl/leave_sec
# 门里不留怪
execute in rpg:paradise_lost positioned 0 83 0 as @e[type=#rpg:elite_pool,distance=..38] unless entity @s[tag=rpg.pl.g] run tp @s ~ -200 ~
# 掠夺者在这里几乎不会自己消失，会把刷怪名额占满：全维度最多留 5 只（河庭的守卫不算）
execute in rpg:paradise_lost positioned 0 83 0 store result score #pc rpg_pl if entity @e[type=minecraft:pillager,distance=0..,tag=!rpg.pl.g,tag=!rpg.el]
execute if score #pc rpg_pl matches 6.. in rpg:paradise_lost positioned 0 83 0 as @e[type=minecraft:pillager,distance=0..,tag=!rpg.pl.g,tag=!rpg.el,sort=random,limit=6] at @s unless entity @a[distance=..14] run tp @s ~ -200 ~
# 搬着方块的末影人不会消失，也会把地面搬乱
execute in rpg:paradise_lost positioned 0 83 0 as @e[type=minecraft:enderman,distance=0..,nbt={carriedBlockState:{}}] run data remove entity @s carriedBlockState
# 新刷出来的怪按离门多远强化
execute in rpg:paradise_lost positioned 0 83 0 as @e[type=#rpg:elite_pool,tag=!rpg.pl.s,distance=36..] at @s run function rpg:pl/mob/see
# 侵蚀：门外每分钟
execute in rpg:paradise_lost positioned 0 83 0 as @a[distance=36..,gamemode=!spectator,gamemode=!creative] run function rpg:pl/erode
function rpg:pl/moon
function rpg:pl/rain/sec
function rpg:pl/cherub/sec
execute if score #c1 rpg_pl matches 1.. run function rpg:pl/court/1/sec
execute if score #c2 rpg_pl matches 1.. run function rpg:pl/court/2/sec
execute if score #c3 rpg_pl matches 1.. run function rpg:pl/court/3/sec
execute if score #c4 rpg_pl matches 1.. run function rpg:pl/court/4/sec
execute if score #built rpg_pl matches 10 in rpg:paradise_lost positioned 0 83 -120 if score #c1 rpg_pl matches 0 if entity @a[distance=..7,gamemode=!spectator] run function rpg:pl/court/1/try
execute if score #built rpg_pl matches 10 in rpg:paradise_lost positioned 120 83 0 if score #c2 rpg_pl matches 0 if entity @a[distance=..5,gamemode=!spectator] run function rpg:pl/court/2/try
execute if score #built rpg_pl matches 10 in rpg:paradise_lost positioned 0 83 120 if score #c3 rpg_pl matches 0 if entity @a[distance=..8,gamemode=!spectator] run function rpg:pl/court/3/try
execute if score #built rpg_pl matches 10 in rpg:paradise_lost positioned -120 83 0 if score #c4 rpg_pl matches 0 if entity @a[distance=..8,gamemode=!spectator] run function rpg:pl/court/4/try
execute store result score #d rpg_pl run time query day
execute in rpg:paradise_lost as @a[x=0,y=83,z=0,distance=36..,gamemode=!spectator] unless score @s rpg_pl_fort = #d rpg_pl at @s if predicate rpg:paradise/in_fortress run function rpg:pl/fortress/enter
