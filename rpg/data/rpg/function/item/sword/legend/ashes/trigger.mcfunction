advancement revoke @s only rpg:item/ashes
execute as @s at @s run scoreboard players add @s ashes_step 1
execute as @s at @s anchored eyes run particle enchant ~0.5 ~0.5 ~0.5 -1 -1 -1 1 50
execute as @s at @s anchored eyes run particle large_smoke ~0.5 ~0.5 ~0.5 -1 -1 -1 0.3 10
execute as @s at @s run xp add @s -1 points
