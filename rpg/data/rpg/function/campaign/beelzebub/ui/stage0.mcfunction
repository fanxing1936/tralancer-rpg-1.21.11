bossbar set rpg:chapter1 color yellow
bossbar set rpg:chapter1 name ["",{"text":"楔子｜第十三声钟","color":"#B8A98B","bold":true,"italic":false}]
execute unless entity @s[tag=rpg.ch1.ui.title.0] run function rpg:campaign/beelzebub/ui/title/stage0
