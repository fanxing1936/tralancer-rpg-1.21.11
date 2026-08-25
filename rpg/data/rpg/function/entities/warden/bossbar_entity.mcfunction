execute unless score @s rpg_boss_slot = @s rpg_boss_slot run function rpg:entities/warden/bossbar_allocate
execute if score @s rpg_boss_slot matches 0 run function rpg:entities/warden/bossbar_allocate
execute if score @s rpg_boss_slot matches 1 run return run function rpg:entities/warden/bossbar_show1
execute if score @s rpg_boss_slot matches 2 run return run function rpg:entities/warden/bossbar_show2
execute if score @s rpg_boss_slot matches 3 run return run function rpg:entities/warden/bossbar_show3
execute if score @s rpg_boss_slot matches 4 run return run function rpg:entities/warden/bossbar_show4
