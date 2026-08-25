# 取第一个空槽；四槽满时稳定落到 0，并在后续 tick 重试。
execute if score #boss_slot1 rpg_boss_slot matches 0 run return run function rpg:entities/warden/bossbar_assign1
execute if score #boss_slot2 rpg_boss_slot matches 0 run return run function rpg:entities/warden/bossbar_assign2
execute if score #boss_slot3 rpg_boss_slot matches 0 run return run function rpg:entities/warden/bossbar_assign3
execute if score #boss_slot4 rpg_boss_slot matches 0 run return run function rpg:entities/warden/bossbar_assign4
scoreboard players set @s rpg_boss_slot 0
