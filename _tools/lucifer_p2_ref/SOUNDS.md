# 原作音效绑定

46 个 Wiki 原 Ogg 保持字节与 SHA 不变：主页面44个，藤蔓补充2个。注册38个声音事件；25个启用的源时间通知进入动画。30条原通知全部逐项校验；另含非声音通知，两个idle SoundCue因原volume=0而静音。

29个 cooked SoundCue 的107个对象用于追踪实际 wave pool。Basic/Vine vocal保留源三项等权池；Walk vocal四分支中两项为空，目标保留50%播放机会；Walk Foley只使用Walk1/2，未误放legacy。源失败藤蔓Foley实际引用成功声，按源记录保留。

| clip | 原通知 | 源秒（含offset） | 事件 | 输出tick | 策略 |
|---|---|---:|---|---:|---|
| jungleAbomination_Attack | DungeonsPlaySound | 0.08685424 | basic_attack_foley | 2 | 已绑定 |
| jungleAbomination_Attack | DungeonsPlaySound | 1.1991489 | basic_attack_voice | 24 | 已绑定 |
| jungleAbomination_Attack | PlayParticleEffect | 1.5364347 | — | — | 非声音通知 |
| jungleAbomination_death | DungeonsPlaySound | 0.0001 | death_foley | 0 | 已绑定 |
| jungleAbomination_death | DungeonsPlaySound | 0.0001 | death_voice | 0 | 已绑定 |
| jungleAbomination_idle | DungeonsPlaySound | 0.058183 | idle_foley | — | 原作静音 |
| jungleAbomination_idle | DungeonsPlaySound | 1.7288662 | idle_voice | — | 原作静音 |
| jungleAbomination_land | DungeonsPlaySound | 0.0001 | land_foley | 0 | 已绑定 |
| jungleAbomination_land | DungeonsPlaySound | 0.0001 | land_voice | 0 | 已绑定 |
| jungleAbomination_land | PlayParticleEffect | 0.037677303 | — | — | 非声音通知 |
| jungleAbomination_summon | DungeonsPlaySound | 0.0001 | summon_foley | 0 | 已绑定 |
| jungleAbomination_summon | DungeonsPlaySound | 0.632495 | summon_voice | 13 | 已绑定 |
| jungleAbomination_vineAttack | DungeonsPlaySound | 0.0001 | vine_attack_foley | 0 | 已绑定 |
| jungleAbomination_vineAttack | DungeonsPlaySound | 1.0380974 | vine_attack_voice | 21 | 已绑定 |
| jungleAbomination_vineAttackSucessful | DungeonsPlaySound | 0.0001 | vine_success_foley | 0 | 已绑定 |
| jungleAbomination_vineAttackSucessful | DungeonsPlaySound | 0.0001 | vine_success_voice | 0 | 已绑定 |
| jungleAbomination_vineAttackUnsucessful | DungeonsPlaySound | 0.0001 | vine_success_foley | 0 | 已绑定 |
| jungleAbomination_vineAttackUnsucessful | DungeonsPlaySound | 0.0001 | vine_fail_voice | 0 | 已绑定 |
| jungleAbomination_vulnerableFall | DungeonsPlaySound | 0.0001 | fall_foley | 0 | 已绑定 |
| jungleAbomination_vulnerableFall | DungeonsPlaySound | 0.0001 | fall_voice | 0 | 已绑定 |
| jungleAbomination_vulnerableFall | DungeonsPlaySound | 0.78448987 | flower_open | 16 | 已绑定 |
| jungleAbomination_vulnerableFall | Trigger Flower LOOP | 0.78448987 | flower_loop | 16 | 已绑定 |
| jungleAbomination_vulnerableGetUp | DungeonsPlaySound | 0.0001 | getup_foley | 0 | 已绑定 |
| jungleAbomination_vulnerableGetUp | DungeonsPlaySound | 0.0001 | flower_close | 0 | 已绑定 |
| jungleAbomination_vulnerableGetUp | Flower LOOP Fade Out | 0.0001 | — | — | 非声音通知 |
| jungleAbomination_vulnerableGetUp | DungeonsPlaySound | 0.3179052 | getup_voice | 6 | 已绑定 |
| jungleAbomination_walk | DungeonsPlaySound | 0.0001 | walk_foley | 0 | 已绑定 |
| jungleAbomination_walk | DungeonsPlaySound | 0.04320923 | walk_voice | 1 | 已绑定 |
| jungleAbomination_walk | DungeonsPlaySound | 1.2404281 | walk_foley | 25 | 已绑定 |
| jungleAbomination_walk | DungeonsPlaySound | 1.2918868 | walk_voice | 26 | 已绑定 |

Flower LOOP来自具名原通知的语义映射：在vulnerableFall通知处启动，87ticks重复一次，在getup、death或离开脆弱状态时取消后续重复。已发出的4.326秒样本可以自然结束；不全局stopsound，以免静音另一Boss。导出的Flower_LOOP SoundCue没有FirstNode，所以不把这一目标循环策略说成已还原源音频图。

源ProjectileAttack及三个Composite没有声音通知，未靠头部回弹猜测发射/音效时刻。Attack_BOOM仅注册供手动试听，原用途未证实。hurt绑定实际载体受伤；death保留源0秒通知，孤儿fallback防止已播放死亡声再次触发。

3段音乐是手动debug预览，Start/Loop仅30秒，不在load/tick/动作自动播放。两个藤蔓附加声只注册，不生成藤蔓实体。固定源音量保留；随机pitch、Unreal衰减、并发、no-repeat历史未完整移植。逐文件来源、精确池和通知见 `validation/sound_binding.json`。
