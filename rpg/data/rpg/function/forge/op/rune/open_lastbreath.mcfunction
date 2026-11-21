execute unless data storage rpg:forge e{kind:"armor"} run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　[余生]只能镶在护甲上","color":"#C04A3C","bold":false,"italic":false}]
execute if data storage rpg:forge e{runes:["lastbreath"]} run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　同一件装备不能镶两枚[余生]","color":"#C04A3C","bold":false,"italic":false}]
scoreboard players set @s rpg_fg_op 5
scoreboard players set @s rpg_fg_arg 10
scoreboard players set #free rpg_fg -1
execute store result score #lv rpg_fg run data get storage rpg:forge e.lv
function rpg:forge/op/rune/free_at {i:0}
execute if score #free rpg_fg matches -1 unless data storage rpg:forge e{kind:"armor"} if score #lv rpg_fg matches 5.. run function rpg:forge/op/rune/free_at {i:1}
execute if score #free rpg_fg matches 0.. run scoreboard players operation @s rpg_fg_arg2 = #free rpg_fg
execute if score #free rpg_fg matches 0.. store result storage rpg:forge d.slot int 1 run scoreboard players add #free rpg_fg 1
execute if score #free rpg_fg matches 1.. run return run function rpg:forge/op/rune/show_lastbreath with storage rpg:forge d
function rpg:forge/op/rune/full
function rpg:forge/op/rune/swap_lastbreath with storage rpg:forge d
