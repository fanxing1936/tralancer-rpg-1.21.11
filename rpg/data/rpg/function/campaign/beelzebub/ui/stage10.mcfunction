bossbar set rpg:chapter1 color yellow
bossbar set rpg:chapter1 name ["",{"text":"第一章完成｜登记为教廷边缘者","color":"#D4AF37","bold":true,"italic":false}]
execute unless entity @s[tag=rpg.ch1.ui.title.10] run function rpg:campaign/beelzebub/ui/title/stage10
