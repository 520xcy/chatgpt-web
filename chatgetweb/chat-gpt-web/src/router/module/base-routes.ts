

export default [
    {
        path: '/',
        component: ()=>import('../../views/chat.vue'),
        meta: { title: '聊天室' }
      }
//   ,{
//     path: '/',
//     redirect: '/console',
//     component: BaseLayout,
//     meta: { title: '工作空间' },
//     children: [
//       {
//         path: '/analysis',
//         component: () => import('../../views/Analysis/index.vue'),
//         meta: { title: '分析页' },
//       },
//       {
//         path: '/console',
//         component: () => import('../../views/Console/index.vue'),
//         meta: { title: '控制台' },
//       }
//     ]
//   }
]