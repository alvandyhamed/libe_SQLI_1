<?php
require('setup.php');

if (isset($_GET['source'])) {
    die(highlight_file(__FILE__));
}


if (isset($_GET['id'])) {
    $sql = "SELECT * FROM news WHERE id = '" . $_GET['id'] . "'";
    $result = $conn->query($sql);
    $post = $result->fetch_assoc();
} else {
    header('Location: index.php');
    exit();
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charSet="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="stylesheet" href="files/global.css">
    <title><?php echo htmlspecialchars($post['title']); ?> - Voorivex Academy</title>
    <meta name="description" content="SQL Injection training environment" />
    <link rel="icon" href="/favicon.ico" type="image/x-icon" sizes="16x16" />
</head>

<body class="__variable_1e4310 __variable_c3aa02 antialiased">
    <main class="min-h-screen bg-[#2d2b33] p-8">
        <div class="max-w-3xl mx-auto space-y-8">
            <header class="text-white">
                <a href="index.php" class="text-[#FFBF00] mb-4 inline-block hover:underline">← Back to Articles</a>
                <?php if ($post): ?>
                    <div class="bg-[#363440] rounded-lg overflow-hidden border border-gray-700 p-8">
                        <div class="mb-6">
                            <div class="flex justify-between items-start mb-4">
                                <h1 class="text-4xl font-bold"><?php echo htmlspecialchars($post['title']); ?></h1>
                                <span class="bg-[#FFBF00] text-black px-3 py-1 rounded-full text-sm font-medium">
                                    <?php echo htmlspecialchars($post['category']); ?>
                                </span>
                            </div>

                            <div class="flex items-center space-x-4 text-gray-400 text-sm mb-6">
                                <span>By <?php echo htmlspecialchars($post['author']); ?></span>
                                <span>•</span>
                                <span><?php echo htmlspecialchars($post['publish_date']); ?></span>
                                <span>•</span>
                                <span>👁 <?php echo htmlspecialchars($post['views']); ?> views</span>
                            </div>

                            <?php if (!empty($post['image_url'])): ?>
                            <div class="w-full h-64 mb-6">
                                <img src="<?php echo htmlspecialchars($post['image_url']); ?>"
                                     alt=""
                                     class="w-full h-full object-cover rounded-lg">
                            </div>
                            <?php endif; ?>

                            <div class="text-gray-300 leading-relaxed space-y-4">
                                <?php echo nl2br(htmlspecialchars($post['content'])); ?>
                            </div>
                        </div>
                    </div>
                <?php else: ?>
                    <div class="bg-[#363440] rounded-lg overflow-hidden border border-gray-700 p-8">
                        <h1 class="text-2xl font-bold text-white mb-4">Article Not Found</h1>
                        <p class="text-gray-400">The requested article could not be found.</p>
                    </div>
                <?php endif; ?>
            </header>
            <footer class="text-center text-gray-400 mt-8">© 2024 Voorivex Academy</footer>
        </div>
    </main>
</body>
</html>
<?php
$conn->close();
?>