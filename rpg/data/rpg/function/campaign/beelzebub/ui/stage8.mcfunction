bossbar set rpg:chapter1 color red
bossbar set rpg:chapter1 name ["",{"text":"裁决落空｜见证人印缺失","color":"#FF806B","bold":true,"italic":false}]
execute if score @s rpg_ch1_time matches 12.. unless entity @s[tag=rpg.ch1.ui.title.8] run function rpg:campaign/beelzebub/ui/title/stage8
execute unless entity @s[tag=rpg.ch1.ui.scene.8] run function rpg:campaign/beelzebub/ui/scene/stage8
