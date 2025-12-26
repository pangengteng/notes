# SEATA

## 分布式事务

> 分布式服务背景下，一个完整的业务逻辑通常需要由几个服务共同完成。比如电商中的下单场景，涉及库存、订单、账户等服务，这些服务之间的数据，也需要像普通事务一样，保持ACID特性。跨服务的事务，是其中一种分布式事务，其他的，像跨异构数据源，例如库存数据同时保存在 Mysql 和 Redis 中，它们之间也需要保证数据一致性，也是一种分布式事务。
>
> SEATA 是阿里巴巴开源的一款支持分布式事务的框架，是我们学习分布式事务的一个不错的选择

## 核心术语

> seata server: 扮演事务协调者（TC: Transaction Coordinator）的角色，负责维护全局事务状态，管理分支事务，协调全局事务提交/回滚
> seata client: 分布式事务参与者，一般是业务应用服务。内部集成分布式事务管理器（TM: Transaction Manager）和资源管理器（RM: Resource Manager），分别负责开启/提交/回滚全局事务，和数据库交互

## 事务模式

> 基于两阶段提交模型
![](images/seata-1.png)

### AT

> 基于支持本地 ACID 事务的关系型数据库。特点是低业务入侵，数据强一致性。由于 RM 需要解析业务 SQL 生成 undo log，一定程度上会影响性能，所以要求业务 SQL 尽量简单。
> 全局事务隔离级别是读未提交

**整体机制**

> 一阶段：注册分支、获取全局锁，提交 undo log 和业务sql
> 二阶段：异步commit，删除 undo log；通过 undo log 回滚

**流程图**
```mermaid
sequenceDiagram
    participant Client as 业务应用（Client）
    participant TM as 事务管理器（TM）
    participant TC as 事务协调器（TC）
    participant RM1 as 资源管理器1（RM1，如数据库A）
    participant RM2 as 资源管理器2（RM2，如数据库B）

    Note over Client, RM2: 一阶段：执行业务 + 分支注册（含全局锁申请）

    Client->>TM: 1. 执行 @GlobalTransactional 方法
    TM->>TC: 2. 同步调用 begin() 开启全局事务
    TC-->>TM: 3. 返回 XID
    TM-->>Client: 4. 透传 XID 到上下文

    Client->>RM1: 5. 执行本地SQL（带XID）
    RM1->>RM1: 6. 解析SQL，生成镜像 + 提取主键（lockKeys）
    RM1->>TC: 7. BranchRegister(XID, resource, lockKeys)
    Note right of TC: TC内部：<br/>- 校验XID<br/>- acquireLock(lockKeys)<br/>- 成功则注册分支
    TC-->>RM1: 8. 分支注册成功
    RM1->>RM1: 9. 执行本地事务（业务数据 + undo_log）
    RM1-->>Client: 10. 本地事务提交

    Client->>RM2: 11. 执行本地SQL（带XID）
    RM2->>RM2: 12. 解析SQL + 提取lockKeys
    RM2->>TC: 13. BranchRegister(XID, resource, lockKeys)
    TC-->>RM2: 14. 分支注册成功
    RM2->>RM2: 15. 执行本地事务（含undo_log）
    RM2-->>Client: 16. 本地事务提交

    Note over Client, TC: 二阶段：TM 同步调用 TC，Client等待结果

    alt 全局提交（快速响应）
        Client->>TM: 17. 业务逻辑成功结束
        TM->>TC: 18. 同步调用 GlobalCommit(XID)
        TC->>TC: 19. ⭐ 立即释放该XID所有全局锁
        TC->>TC: 20. 状态置为 Committing
        TC-->>TM: 21. 返回 GlobalStatus.Committed
        TM-->>Client: 22. ✅ 方法正常返回（Client收到成功）
        
        TC->>RM1: 23. 异步通知 branchCommit（后台）
        TC->>RM2: 24. 异步通知 branchCommit
        RM1->>RM1: 25. 后台异步删除 undo_log
        RM2->>RM2: 26. 后台异步删除 undo_log
        TC->>TC: 27. [✅ 全局事务结束]<br/>状态：Committed（会话清理）

    else 全局回滚（同步等待）
        Client->>TM: 17'. 业务抛出异常
        TM->>TC: 18'. 同步调用 GlobalRollback(XID)
        
        TC->>RM1: 19'. 同步调用 branchRollback
        RM1->>RM1: 20'. 执行反向SQL回滚 + 删除undo_log
        RM1-->>TC: 21'. 返回 BranchStatus.Rollbacked
        TC->>TC: 22'. 释放RM1对应的全局锁

        TC->>RM2: 23'. 同步调用 branchRollback
        RM2->>RM2: 24'. 执行回滚 + 删除undo_log
        RM2-->>TC: 25'. 返回成功
        TC->>TC: 26'. 释放RM2对应的全局锁

        TC->>TC: 27'. 状态置为 Rollbacked
        TC-->>TM: 28'. 返回 GlobalStatus.Rollbacked
        TM-->>Client: 29'. ❌ 方法抛出异常（Client收到失败）
        TC->>TC: 30. [✅ 全局事务结束]<br/>状态：Rollbacked（或 RollbackFailed）
    end

    Note over TM, Client: ⏱️ Client 的响应时间：<br/>- 提交：极短（仅TC内部操作）<br/>- 回滚：较长（含RM回滚耗时）
```

### TCC

> 属于在服务层实现全局事务，不依赖具体的事务资源（数据库），但需要业务实现具体的 try-confirm-cancel 方法。特点是高业务入侵，数据强一致性，高性能。常见的跨资源 Redis / 消息队列 / Mysql 场景下可以使用该模式

**流程图**
```mermaid
sequenceDiagram
    participant Client as 业务应用（Client）
    participant TM as 事务管理器（TM）
    participant TC as 事务协调器（TC）
    participant Proxy1 as TCC代理1（Seata AOP）
    participant Biz1 as 业务实现1（如OrderService）
    participant Proxy2 as TCC代理2
    participant Biz2 as 业务实现2（如InventoryService）

    Note over Client, Biz2: 一阶段：全局事务开启 + Try 阶段

    Client->>TM: 1. 执行 @GlobalTransactional 方法
    TM->>TC: 2. 同步调用 begin()，申请XID
    TC-->>TM: 3. 返回全局事务ID（XID）
    TM-->>Client: 4. 透传 XID 到上下文

    Client->>Proxy1: 5. 调用 @TwoPhaseBusinessAction 方法（如 createOrder）
    Proxy1->>TC: 6. ⭐ 自动 BranchRegister(XID, resourceID, null)<br/>（TCC 不申请全局锁）
    TC-->>Proxy1: 7. 分支注册成功
    Proxy1->>Biz1: 8. 执行业务 Try 逻辑
    Biz1->>Biz1: 9. 预留资源（如冻结库存、生成预留单）
    Biz1-->>Proxy1: 10. Try 成功
    Proxy1-->>Client: 11. 返回成功

    Client->>Proxy2: 12. 调用另一个 TCC 方法（如 freezeStock）
    Proxy2->>TC: 13. ⭐ 自动 BranchRegister(XID, resourceID, null)
    TC-->>Proxy2: 14. 分支注册成功
    Proxy2->>Biz2: 15. 执行 Try 逻辑
    Biz2->>Biz2: 16. 预留资源（如冻结金额）
    Biz2-->>Proxy2: 17. Try 成功
    Proxy2-->>Client: 18. 返回成功

    Note over Client, TC: 二阶段：根据结果 Confirm 或 Cancel

    alt 所有Try成功 → 全局提交
        Client->>TM: 19. 业务逻辑成功结束
        TM->>TC: 20. 同步调用 GlobalCommit(XID)
        TC-->>TM: 21. 返回 GlobalStatus.Committed（快速）
        TM-->>Client: 22. ✅ 方法正常返回

        TC->>Proxy1: 23. 异步调用 confirm(XID)
        Proxy1->>Biz1: 24. 执行确认（如扣减库存）
        Biz1-->>Proxy1: 25. 确认成功

        TC->>Proxy2: 26. 异步调用 confirm(XID)
        Proxy2->>Biz2: 27. 执行确认（如扣款）
        Biz2-->>Proxy2: 28. 确认成功

        TC->>TC: 29. [✅ 全局事务结束]<br/>状态：Committed

    else 任一Try失败 → 全局回滚
        Client->>TM: 19'. 业务异常（如Biz2.Try失败）
        TM->>TC: 20'. 同步调用 GlobalRollback(XID)

        TC->>Proxy1: 21'. 同步调用 cancel(XID)
        Proxy1->>Biz1: 22'. 执行 Cancel（如释放冻结库存）
        Biz1-->>Proxy1: 23'. 返回成功

        TC->>Proxy2: 24'. 同步调用 cancel(XID)
        Proxy2->>Biz2: 25'. 执行 Cancel（如解冻金额）
        Biz2-->>Proxy2: 26'. 返回成功

        TC-->>TM: 27'. 返回 GlobalStatus.Rollbacked
        TM-->>Client: 28'. ❌ 方法抛出异常
        TC->>TC: 29. [✅ 全局事务结束]<br/>状态：Rollbacked（或失败）
    end

    Note right of Biz1: 💡 业务需自行实现：<br/>- 幂等性<br/>- 空回滚（Cancel时Try未执行）<br/>- 防悬挂（Cancel先于Try）
    Note right of TC: 🔒 TCC 无全局锁，<br/>靠业务预留资源保证隔离性
```

### SAGA

### XA