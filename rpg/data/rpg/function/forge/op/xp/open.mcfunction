execute if data storage rpg:forge e{lv:10} run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　这件装备已经满级，铸造之石用不上","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set @s rpg_fg_op 1
execute store result score #lv rpg_fg run data get storage rpg:forge e.lv
execute store result score #xp rpg_fg run data get storage rpg:forge e.xp
execute store result storage rpg:forge d.lv0 int 1 run scoreboard players get #lv rpg_fg
execute store result storage rpg:forge d.xp0 int 1 run scoreboard players get #xp rpg_fg
scoreboard players add #xp rpg_fg 100
scoreboard players set #up rpg_fg 0
function rpg:forge/xp/loop
scoreboard players operation #need rpg_fg = #lv rpg_fg
scoreboard players operation #need rpg_fg *= #20 rpg_fg
execute store result storage rpg:forge d.lv1 int 1 run scoreboard players get #lv rpg_fg
execute store result storage rpg:forge d.xp1 int 1 run scoreboard players get #xp rpg_fg
execute store result storage rpg:forge d.need int 1 run scoreboard players get #need rpg_fg
function rpg:forge/op/xp/show with storage rpg:forge d
