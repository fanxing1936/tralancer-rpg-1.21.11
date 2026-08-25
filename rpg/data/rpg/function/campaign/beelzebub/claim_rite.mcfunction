tag @s add rpg.ch1.rite
scoreboard players operation @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current,sort=nearest,limit=1,distance=..14] rpg_ch1_id
tellraw @a[tag=rpg.ch1.current,distance=..20] ["",{"text":"[Ⅱ · 镇魔] ","color":"#D4AF37","bold":true,"italic":false},{"text":"真名与点燃图腾已经将祂绑定。","color":"gray","bold":false,"italic":false}]
