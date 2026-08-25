function rpg:inquest/tool/place/medium5
function rpg:inquest/consume_offer
tag @s add rpg.rite.medium
scoreboard players add @s rpg_ex_stab 25
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
scoreboard players add @a[distance=..8,gamemode=!spectator] rpg_ex_xp 6
function rpg:inquest/stability/show
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[弱点媒介] ","color":"#7B241C","italic":false,"bold":true},{"text":"雪球 · 熄怒之雪已布入法阵，稳定度上升。","color":"gray","italic":false}]
playsound minecraft:block.enchantment_table.use player @a[distance=..20] ~ ~ ~ 1 0.7
