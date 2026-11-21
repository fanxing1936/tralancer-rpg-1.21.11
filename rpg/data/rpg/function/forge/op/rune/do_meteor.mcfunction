execute if score #do rpg_fg matches 10 run scoreboard players set @s rpg_fg_arg2 0
execute if score #do rpg_fg matches 11 run scoreboard players set @s rpg_fg_arg2 1
execute if score #do rpg_fg matches 11 if data storage rpg:forge e{kind:"armor"} run return 0
execute store result score #lv rpg_fg run data get storage rpg:forge e.lv
execute if score @s rpg_fg_arg2 matches 1 if score #lv rpg_fg matches ..4 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　第二个符文槽要到 Lv.5 才解锁","color":"#C04A3C","bold":false,"italic":false}]
execute if data storage rpg:forge e{runes:["meteor"]} run return 0
execute store result storage rpg:forge g.i int 1 run scoreboard players get @s rpg_fg_arg2
data modify storage rpg:forge g.v set value "meteor"
function rpg:forge/op/rune/put with storage rpg:forge g
function rpg:forge/render
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
function rpg:forge/ui/done
