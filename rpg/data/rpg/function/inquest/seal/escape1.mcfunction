clear @s minecraft:echo_shard[minecraft:food={nutrition:0,saturation:0f,can_always_eat:1b},minecraft:consumable={consume_seconds:100160f,animation:"block",sound:"minecraft:block.respawn_anchor.ambient",has_consume_particles:false,on_consume_effects:[]},minecraft:max_stack_size=1,minecraft:custom_data~{rpg_sealed:1b,rpg_lord:1}] 1
scoreboard players add @s rpg_taint 15
execute at @s run function rpg:taint/lord1
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[封印逃逸] ","color":"#00491C","bold":true,"italic":false},{"text":"路西法的残魂从遗物中重新降临。","color":"gray","italic":false}]
playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..32] ~ ~ ~ 1 0.55
function rpg:inquest/seal/reindex
