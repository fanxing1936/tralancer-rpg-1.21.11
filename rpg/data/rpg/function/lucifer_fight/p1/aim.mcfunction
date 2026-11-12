summon minecraft:marker ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.mark","rpg.lu1f.aim","rpg.lu2f.new"]}
execute as @e[type=minecraft:marker,tag=rpg.lu2f.new,tag=rpg.lu1f.aim] at @s facing entity @a[distance=..24,gamemode=!spectator,gamemode=!creative,limit=1,sort=nearest] feet run tp @s ~ ~ ~ ~ 0
scoreboard players operation @e[tag=rpg.lu2f.new] rpg_l2_id = @s rpg_l2_id
scoreboard players set @e[tag=rpg.lu2f.new] rpg_l2_t 60
tag @e[tag=rpg.lu2f.new] remove rpg.lu2f.new
