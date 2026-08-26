bossbar set rpg:chapter1 value 94
bossbar set rpg:chapter1 name ["",{"text":"活着的人必须有名字｜救下米拉","color":"#8B2500","bold":true,"italic":false}]
execute positioned ^ ^ ^8 run summon minecraft:villager ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.witness","rpg.vac.seen","rpg.ch1.new"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:["",{"text":"米拉 · 真实见证人","color":"#FFF2A8","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:villager,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..20] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:villager,tag=rpg.ch1.new] remove rpg.ch1.new
tellraw @a[tag=rpg.ch1.current] ["",{"text":"审判官 塞维拉：","color":"#D4AF37","bold":true,"italic":false},{"text":"所有见证人都是污染源。包括她，也包括你。","color":"gray","bold":false,"italic":false}]

function rpg:campaign/beelzebub/ui/scene/clear
