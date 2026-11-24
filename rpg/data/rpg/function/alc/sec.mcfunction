scoreboard players set #t rpg_alc 0
scoreboard players remove @a[scores={rpg_po_sh=1..}] rpg_po_sh 1
execute as @a[scores={rpg_po_sh=0}] run function rpg:alc/fx/shadow_off
scoreboard players remove @a[scores={rpg_po_bl=1..}] rpg_po_bl 1
execute as @a[scores={rpg_po_bl=1..}] at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.01 4
scoreboard players remove @a[scores={rpg_po_ud=1..}] rpg_po_ud 1
execute as @a[scores={rpg_po_ud=1..}] at @s run particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.01 2
scoreboard players remove @a[scores={rpg_po_lu=1..}] rpg_po_lu 1
