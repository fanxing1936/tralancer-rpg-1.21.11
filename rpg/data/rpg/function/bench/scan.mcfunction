scoreboard players set #t rpg_bn 0
execute as @a[gamemode=!spectator] unless items entity @s weapon.mainhand * at @s anchored eyes positioned ^ ^ ^ run function rpg:bench/look
