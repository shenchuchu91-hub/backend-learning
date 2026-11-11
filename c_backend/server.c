/**
 * @file server.c
 * @brief 基于 Linux POSIX Socket 的极简 HTTP 响应服务器
 * 帮助理解后端底层原理：Socket 套接字、Bind、Listen、Accept、系统调用与多路复用基础
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 8080
#define BUFFER_SIZE 4096

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];

    // 1. 创建套接字 (IPv4, TCP 协议)
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        perror("socket 创建失败");
        exit(EXIT_FAILURE);
    }

    // 设置端口复用（避免重启时提示 Address already in use）
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    // 2. 绑定 IP 与 端口（仅监听 127.0.0.1，避免暴露到局域网或公网）
    server_addr.sin_family = AF_INET;
    if (inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr) != 1) {
        perror("inet_pton 解析 127.0.0.1 失败");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    server_addr.sin_port = htons(PORT);       // 端口转为网络字节序(大端)

    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind 绑定端口失败");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // 3. 开启监听队列
    if (listen(server_fd, 10) < 0) {
        perror("listen 监听失败");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("====================================================\n");
    printf(" [C 语言底层网络服务器已启动]\n");
    printf(" 监听地址: http://127.0.0.1:%d\n", PORT);
    printf(" 正在等待客户端连接 (按 Ctrl + C 退出)...\n");
    printf("====================================================\n\n");

    // 4. 事件循环：接收并处理请求
    while (1) {
        client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) {
            perror("accept 连接接收失败");
            continue;
        }

        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, INET_ADDRSTRLEN);
        printf("[收到新连接] 来自: %s:%d\n", client_ip, ntohs(client_addr.sin_port));

        memset(buffer, 0, BUFFER_SIZE);
        ssize_t bytes_read = read(client_fd, buffer, BUFFER_SIZE - 1);
        if (bytes_read > 0) {
            // 打印请求头第一行 (例如: GET / HTTP/1.1)
            char *line_end = strstr(buffer, "\r\n");
            if (line_end) {
                *line_end = '\0';
                printf(" > 请求方法及路径: %s\n", buffer);
            }

            // 构造标准 HTTP 响应报文
            const char *http_body = 
                "{\n"
                "  \"code\": 200,\n"
                "  \"message\": \"Hello from C Socket Server!\",\n"
                "  \"tip\": \"你已经触碰到了后端网络服务最核心的 Socket 层!\"\n"
                "}\n";

            char http_response[BUFFER_SIZE];
            snprintf(http_response, sizeof(http_response),
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json; charset=utf-8\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s",
                strlen(http_body), http_body
            );

            // 发送数据并关闭连接
            write(client_fd, http_response, strlen(http_response));
        }

        close(client_fd);
    }

    close(server_fd);
    return 0;
}
