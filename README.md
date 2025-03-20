<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kasa Smart Plug Controller</title>
</head>
<body>
    <h1>ตัวควบคุม Kasa Smart Plug</h1>
    <p>แอปพลิเคชันเว็บที่พัฒนาด้วย Flask เพื่อค้นหาและควบคุมปลั๊กอัจฉริยะ TP-Link Kasa บนเครือข่ายท้องถิ่นของคุณ โครงการนี้ช่วยให้คุณเปิดหรือปิดอุปกรณ์ได้ผ่านคำขอ HTTP GET แบบง่ายๆ</p>

    <h2>คุณสมบัติ</h2>
    <ul>
        <li>ค้นหาปลั๊กอัจฉริยะ Kasa บนเครือข่ายโดยใช้ไลบรารี <code>python-kasa</code></li>
        <li>ควบคุมปลั๊กอัจฉริยะ (เปิด/ปิด) ผ่าน endpoints แบบ RESTful</li>
        <li>ดึงข้อมูลอุปกรณ์ เช่น ที่อยู่ IP, ชื่อ alias และรุ่นของอุปกรณ์</li>
        <li>รองรับการใช้ตัวแปรสภาพแวดล้อมเพื่อจัดการข้อมูลรับรองอย่างปลอดภัย</li>
    </ul>

    <h2>สิ่งที่ต้องเตรียม</h2>
    <ul>
        <li>Python 3.7 หรือสูงกว่า</li>
        <li>ปลั๊กอัจฉริยะ TP-Link Kasa ที่เชื่อมต่อกับเครือข่ายท้องถิ่นของคุณ</li>
        <li>บัญชี Kasa (ชื่อผู้ใช้และรหัสผ่าน)</li>
    </ul>

    <h2>การติดตั้ง</h2>
    <ol>
        <li>
            <strong>โคลน repository</strong><br>
            <pre><code>git clone https://github.com/yourusername/kasa-smart-plug-controller.git

cd kasa-smart-plug-controller</code></pre>

</li>
<li>
<strong>ตั้งค่าสภาพแวดล้อมเสมือน</strong> (แนะนำแต่ไม่บังคับ)<br>
<pre><code>python -m venv venv
source venv/bin/activate # บน Windows: venv\Scripts\activate</code></pre>
</li>
<li>
<strong>ติดตั้ง dependencies</strong><br>
<pre><code>pip install -r requirements.txt</code></pre>
หากยังไม่มีไฟล์ <code>requirements.txt</code> ให้ติดตั้งแพ็กเกจที่จำเป็นด้วยตนเอง:<br>
<pre><code>pip install flask python-kasa</code></pre>
</li>
<li>
<strong>ตั้งค่าตัวแปรสภาพแวดล้อม</strong><br> - สร้างไฟล์ <code>.env</code> หรือกำหนดตัวแปรสภาพแวดล้อมสำหรับชื่อผู้ใช้และรหัสผ่าน Kasa:<br>
<pre><code>export KASA_USERNAME="your_kasa_email"
export KASA_PASSWORD="your_kasa_password"</code></pre> - บน Windows ใช้คำสั่ง:<br>
<pre><code>set KASA_USERNAME="your_kasa_email"
set KASA_PASSWORD="your_kasa_password"</code></pre>
</li>
</ol>

    <h2>การใช้งาน</h2>
    <ol>
        <li>
            <strong>รันแอปพลิเคชัน</strong><br>
            <pre><code>python app.py</code></pre>
            แอปจะทำงานที่ <code>http://0.0.0.0:5001</code> (สามารถเข้าถึงได้จากเครื่องในเครือข่ายเดียวกัน)
        </li>
        <li>
            <strong>Endpoints</strong><br>
            <ul>
                <li><strong>ตรวจสอบสถานะอุปกรณ์</strong>:<br>
                    <code>GET http://&lt;your-ip&gt;:5001/</code><br>
                    คำตอบตัวอย่าง:<br>
                    <pre><code>{"ip": "192.168.1.100", "user": "your_email", "model": "HS100"}</code></pre>
                </li>
                <li><strong>เปิดอุปกรณ์</strong>:<br>
                    <code>GET http://&lt;your-ip&gt;:5001/on</code><br>
                    คำตอบตัวอย่าง:<br>
                    <pre><code>{"status": "Device turned on"}</code></pre>
                </li>
                <li><strong>ปิดอุปกรณ์</strong>:<br>
                    <code>GET http://&lt;your-ip&gt;:5001/off</code><br>
                    คำตอบตัวอย่าง:<br>
                    <pre><code>{"status": "Device turned off"}</code></pre>
                </li>
            </ul>
        </li>
        <li>
            <strong>ข้อผิดพลาด</strong><br>
            - หากไม่พบอุปกรณ์ จะได้รับคำตอบ:<br>
            <pre><code>{"error": "No device found"}</code></pre>
        </li>
    </ol>

    <h2>การแก้ไขปัญหา</h2>
    <ul>
        <li>หากอุปกรณ์ไม่ถูกค้นพบ:
            <ul>
                <li>ตรวจสอบว่าปลั๊ก Kasa อยู่ในเครือข่ายเดียวกันกับเครื่องที่รันแอป</li>
                <li>ตรวจสอบว่าชื่อผู้ใช้และรหัสผ่านถูกต้อง</li>
                <li>ลองเพิ่มค่า <code>discovery_timeout</code> ในโค้ด (เช่น จาก 1 เป็น 5 วินาที)</li>
            </ul>
        </li>
    </ul>

    <h2>การสนับสนุน</h2>
    <p>ใช้ <a href="https://python-kasa.readthedocs.io/">python-kasa documentation</a> สำหรับข้อมูลเพิ่มเติมเกี่ยวกับไลบรารี<br>
    หากมีคำถามหรือปัญหา เปิด issue ใน repository นี้</p>

    <h2>ผู้พัฒนา</h2>
    <p>[PUPAN Ref] (https://github.com/marcellomaugeri/Tapo-Plug-Rest-API)</p>

    <h2>สัญญาอนุญาต</h2>
    <p>โปรเจกต์นี้อยู่ภายใต้ [สัญญาอนุญาตที่คุณเลือก เช่น MIT License]<br>
    ดูรายละเอียดเพิ่มเติมในไฟล์ <code>LICENSE</code></p>

</body>
</html>
