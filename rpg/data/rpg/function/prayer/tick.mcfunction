scoreboard players enable @a rpg_pray
execute as @a[scores={rpg_pr_time=1..}] at @s run function rpg:prayer/animate
execute as @a[scores={rpg_pray=1}] at @s run function rpg:prayer/menu
execute as @a[scores={rpg_pray=2}] at @s run function rpg:prayer/start
execute as @a[scores={rpg_pray=3}] at @s run function rpg:prayer/pool
execute as @a[scores={rpg_pray=4}] at @s run function rpg:prayer/claim
scoreboard players set @a[scores={rpg_pray=1..}] rpg_pray 0
