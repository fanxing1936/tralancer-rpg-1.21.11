bossbar set rpg:chapter1 color yellow
bossbar set rpg:chapter1 name ["",{"text":"辨认空缺者｜以圣器照见异常","color":"#B8A98B","bold":true,"italic":false}]
execute unless entity @s[tag=rpg.ch1.ui.title.2] run function rpg:campaign/beelzebub/ui/title/stage2
