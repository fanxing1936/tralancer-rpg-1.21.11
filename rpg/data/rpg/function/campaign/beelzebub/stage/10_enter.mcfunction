bossbar set rpg:chapter1 value 98
bossbar set rpg:chapter1 name ["",{"text":"边缘者登记｜选择驱魔道路后完成归档","color":"#D4AF37","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"塞维拉：","color":"#D4AF37","bold":true,"italic":false},{"text":"加入边缘者体系，或者作为污染源被处决。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"这不叫选择。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"塞维拉：","color":"#D4AF37","bold":true,"italic":false},{"text":"边缘者从来没有选择。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[打开驱魔师档案并选择道路]","color":"#FFF2A8","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_panel set 1"},"hover_event":{"action":"show_text","value":{"text":"审判、守护或秘仪","color":"gray","bold":false,"italic":false}}}]
execute as @a[tag=rpg.ch1.current,scores={rpg_ex_path=0}] run function rpg:inquest/career
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[归档规则] ","color":"#B8A98B","bold":true,"italic":false},{"text":"至少保留 30 秒选择窗口；未选择道路时章节不会自动结算。","color":"gray","bold":false,"italic":false}]
