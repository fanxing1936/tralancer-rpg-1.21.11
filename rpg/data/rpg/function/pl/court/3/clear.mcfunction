# 这一层过了（at 中心）
scoreboard players set #c3 rpg_pl 2
scoreboard players set #r3 rpg_pl 0
execute as @a[distance=..32,gamemode=!spectator] run scoreboard players add @s rpg_ex_xp 3
execute as @a[distance=..32,gamemode=!spectator] run function rpg:events/bt/trial
playsound minecraft:block.trial_spawner.about_to_spawn_item master @a[distance=..32] ~ ~ ~ 1 1.2
execute if score #l3 rpg_pl matches 5.. run function rpg:pl/court/3/done
