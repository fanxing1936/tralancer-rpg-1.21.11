function rpg:inquest/tool/place/page
tag @s add rpg.rite.page
scoreboard players add @s rpg_ex_stab 10
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
scoreboard players add @a[tag=rpg.rite.user,distance=..6,limit=1] rpg_ex_xp 2
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
