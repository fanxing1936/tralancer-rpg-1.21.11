execute if entity @s[tag=rpg.ch1.rite] if score @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_ch1_id if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_rite_id run return run function rpg:campaign/beelzebub/verdict/banish
tag @s add rpg.rite.anchor.active
scoreboard players add @a[tag=rpg.rite.chooser,distance=..10] rpg_ex_xp 20
tellraw @a[distance=..20,gamemode=!spectator] ["",{"text":"[裁决·放逐] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"完整判词将恶魔逐离此世。","color":"gray","italic":false}]
function rpg:inquest/anchor_success
